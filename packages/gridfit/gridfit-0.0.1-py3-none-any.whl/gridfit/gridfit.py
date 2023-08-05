"""Surface Fitting using gridfit

A python port from the [gridfit](https://www.mathworks.com/matlabcentral/fileexchange/8998-surface-fitting-using-gridfit)
package on Mathworks File Exchange.

Original Author: John D'Errico (woodchips@rochester.rr.com)
"""
import typing as tp
from numbers import Number
from warnings import warn
from dataclasses import dataclass, field
from tqdm.auto import tqdm
import numpy as np
import numpy.typing as npt
from scipy import sparse
import scipy.sparse.linalg
import scipy.linalg


class ParamsError(Exception):
    """Exceptions in Validating Parameter Values for GridFit"""


@dataclass
class Params:
    """Parameters for GridFit"""

    smoothness: tp.Union[Number, npt.ArrayLike] = 1.0
    """Smoothness of the estimated surface

    A larger value here means the surface will be smoother. Smoothness
    must be a non-negative real number.

    If this parameter is a vector of length 2, then it defines
    the relative smoothing to be associated with the x and y
    variables. This allows the user to apply a different amount
    of smoothing in the x dimension compared to the y dimension.

    Note
    ----
    The problem is normalized in advance so that a
    smoothness of 1 MAY generate reasonable results. If you
    find the result is too smooth, then use a smaller value
    for this parameter. Likewise, bumpy surfaces suggest use
    of a larger value. (Sometimes, use of an iterative solver
    with too small a limit on the maximum number of iterations
    will result in non-convergence.)
    """

    interp: tp.Literal["bilinear", "triangle", "nearest"] = "triangle"
    """Interpolation scheme used to interpolate the data.

    1. 'bilinear': use bilinear interpolation within the grid
       (also known as tensor product linear interpolation)
    2. 'triangle': split each cell in the grid into a triangle,
       then linear interpolation inside each triangle
    3. 'nearest': nearest neighbor interpolation. This will
       rarely be a good choice, but I included it
       as an option for completeness.

    """

    regularizer: tp.Literal[
        "diffusion", "laplacian", "gradient", "springs"
    ] = "gradient"
    """Regularization paradignm to be used.

    1. 'diffusion' or 'laplacian': uses a finite difference
       approximation to the Laplacian operator (i.e, del^2).

       .. note::
           We can think of the surface as a plate, wherein the
           bending rigidity of the plate is specified by the user
           as a number relative to the importance of fidelity to
           the data. A stiffer plate will result in a smoother
           surface overall, but fit the data less well. I've
           modeled a simple plate using the Laplacian, del^2. (A
           projected enhancement is to do a better job with the
           plate equations.)
           We can also view the regularizer as a diffusion problem,
           where the relative thermal conductivity is supplied.
           Here interpolation is seen as a problem of finding the
           steady temperature profile in an object, given a set of
           points held at a fixed temperature. Extrapolation will
           be linear. Both paradigms are appropriate for a Laplacian
           regularizer.

    2. 'gradient': attempts to ensure the gradient is as smooth
       as possible everywhere. Its subtly different from the
       'diffusion' option, in that here the directional
       derivatives are biased to be smooth across cell
       boundaries in the grid.

       .. note::
         The gradient option uncouples the terms in the Laplacian.
         Think of it as two coupled PDEs instead of one PDE. Why
         are they different at all? The terms in the Laplacian
         can balance each other.

    3. 'springs': uses a spring model connecting nodes to each
       other, as well as connecting data points to the nodes
       in the grid. This choice will cause any extrapolation
       to be as constant as possible.

       .. note::
         Here the smoothing parameter is the relative stiffness
         of the springs connecting the nodes to each other compared
         to the stiffness of a spting connecting the lattice to
         each data point. Since all springs have a rest length
         (length at which the spring has zero potential energy)
         of zero, any extrapolation will be minimized.

       .. warning::
         The 'springs' regularizer tends to drag the surface
         towards the mean of all the data, so too large a smoothing
         parameter may be a problem.

    """

    solver: tp.Literal["backslash", "lsqr", "normal"] = "backslash"
    """Solver used for the resulting linear system

    Different solvers will have
    different solution times depending upon the specific
    problem to be solved. Up to a certain size grid, the
    direct \ solver will often be speedy, until memory
    swaps causes problems.

    What solver should you use? Problems with a significant
    amount of extrapolation should avoid lsqr. \ may be
    best numerically for small smoothnesss parameters and
    high extents of extrapolation.

    Large numbers of points will slow down the direct
    \, but when applied to the normal equations, \ can be
    quite fast. Since the equations generated by these
    methods will tend to be well conditioned, the normal
    equations are not a bad choice of method to use. Beware
    when a small smoothing parameter is used, since this will
    make the equations less well conditioned.

    1. 'lsqr': uses scipy.sparse.lsqr
    2. 'normal: uses scipy.sparse.lstsq
    """

    maxiter: int = None
    """Maximum number of iterations for an iterative solver

    Default to `min(10000,length(xnodes)*length(ynodes))` if not specified.
    """

    extend: tp.Literal["warning", "never", "always"] = "warning"
    """Controls how boundary nodes are adjusted to bound the data

    1. 'warning': Adjust the first and/or last node in
       x or y if the nodes do not FULLY contain
       the data. Issue a warning message to this
       effect, telling the amount of adjustment
       applied.
    2. 'never': Issue an error message when the nodes do
       not absolutely contain the data.
    3. 'always': automatically adjust the first and last
       nodes in each dimension if necessary.
       No warning is given when this option is set.
    """

    tilesize: int = np.inf
    """Tile size for solving very large grids

    Grids which are simply too large to solve for
    in one single estimation step can be built as a set
    of tiles. For example, a 1000x1000 grid will require
    the estimation of 1e6 unknowns. This is likely to
    require more memory (and time) than you have available.
    But if your data is dense enough, then you can model
    it locally using smaller tiles of the grid.

    My recommendation for a reasonable tilesize is
    roughly 100 to 200. Tiles of this size take only
    a few seconds to solve normally, so the entire grid
    can be modeled in a finite amount of time. The minimum
    tilesize can never be less than 3, although even this
    size tile is so small as to be ridiculous.

    If your data is so sparse than some tiles contain
    insufficient data to model, then those tiles will
    be left as NaNs.
    """

    overlap: Number = 0.20
    """Overlap between tiles

    Tiles in a grid have some overlap, so they
    can minimize any problems along the edge of a tile.
    In this overlapped region, the grid is built using a
    bi-linear combination of the overlapping tiles.

    The overlap is specified as a fraction of the tile
    size, so an overlap of 0.20 means there will be a 20#
    overlap of successive tiles. I do allow a zero overlap,
    but it must be no more than 1/2.

    0 <= overlap <= 0.5

    Overlap is ignored if the tilesize is greater than the
    number of nodes in both directions.
    """

    autoscale: bool = True
    """Autoscale scale data to help regularization

    Some data may have widely different scales on
    the respective x and y axes. If this happens, then
    the regularization may experience difficulties.

    If `True`, will cause gridfit to scale the x
    and y node intervals to a unit length. This should
    improve the regularization procedure. The scaling is
    purely internal.
    """

    mask: npt.NDArray[np.bool_] = None
    """A binary mask that controls which points should be used in gridfit

    Must have the same shape as `xnodes`, `ynodes` arguments in the
    :py:func:`gridfit` function.
    """

    xscale: Number = field(default=1.0, init=False)
    """Scaling of datapoints in the x direction.

    If `autoscale` is `True`, this value is set to the average value of x data points.
    """

    yscale: Number = field(default=1.0, init=False)
    """Scaling of datapoints in the y direction.

    If `autoscale` is `True`, this value is set to the average value of y data points.
    """

    def __post_init__(self):
        if self.smoothness is None:
            self.smoothness = 1.0
        else:
            if np.isscalar(self.smoothness):
                pass
            else:
                if (len(self.smoothness) > 2) or np.any(self.smoothness <= 0):
                    raise ParamsError(
                        "Smoothness must be scalar (or length 2 vector), real, finite, and positive."
                    )
                self.smoothness = np.asarray(self.smoothness)

        # regularizer  - must be one of 4 options - the second and
        # third are actually synonyms.
        valid = ["springs", "diffusion", "laplacian", "gradient"]
        if self.regularizer is None:
            self.regularizer = "diffusion"
        assert self.regularizer in valid, ParamsError(
            f"Invalid regularization method: '{self.regularizer}'"
        )

        # interp must be one of:
        #    'bilinear', 'nearest', or 'triangle'
        # but accept any shortening thereof.
        valid = ["bilinear", "nearest", "triangle"]
        if self.interp is None:
            self.interp = "triangle"

        assert self.interp in valid, ParamsError(
            f"Invalid interpolation method: '{self.interp}'"
        )

        # solver must be one of:
        #    'backslash', 'lsqr', or 'normal'
        # but accept any shortening thereof.
        valid = ["backslash", "lsqr", "normal"]
        if self.solver is None:
            self.solver = "backslash"
        assert self.solver in valid, ParamsError(
            f"Invalid solver option: '{self.solver}'"
        )

        # extend must be one of:
        #    'never', 'warning', 'always'
        # but accept any shortening thereof.
        valid = ["never", "warning", "always"]
        if self.extend is None:
            self.extend = "warning"

        assert self.extend in valid, ParamsError(
            f"Invalid extend option: '{self.extend}'"
        )

        # tilesize == inf by default
        if self.tilesize is None:
            self.tilesize = np.inf
        else:
            assert np.isscalar(self.tilesize) and self.tilesize >= 3, ParamsError(
                f"Tilesize must be scalar and >= 3, got '{self.tilesize}'"
            )

        # overlap == 0.20 by default
        if self.overlap is None:
            self.overlap = 0.20
        else:
            assert (
                np.isscalar(self.overlap) and (self.overlap > 0) and (self.overlap < 1)
            ), ParamsError("Overlap must be scalar and 0 < overlap < 1.")


def gridfit(
    x: npt.NDArray,
    y: npt.NDArray,
    z: npt.NDArray,
    xnodes: npt.NDArray,
    ynodes: npt.NDArray,
    **kwargs,
):
    """Estimates a surface on a 2d grid, based on scattered data

    Gridfit is not an interpolant. It uses a modified ridge estimator
    to generate a surface, where the bias is toward smoothness.

    All methods extrapolate to the grid boundaries.

    Parameters
    ----------
    x,y,z: vectors of equal lengths, containing arbitrary scattered data
      The only constraint on x and y is they cannot ALL fall on a
      single line in the x-y plane. Replicate points will be treated
      in a least squares sense.

      .. note::
        Replicates are allowed.
        Any points containing a NaN are ignored in the estimation

    xnodes: vector defining the nodes in the grid in the independent
      variable (x). xnodes need not be equally spaced. xnodes
      must completely span the data. If they do not, then the
      'extend' property is applied, adjusting the first and last
      nodes to be extended as necessary. See below for a complete
      description of the 'extend' property.
      If xnodes is a scalar integer, then it specifies the number
      of equally spaced nodes between the min and max of the data.

    ynodes: vector defining the nodes in the grid in the independent
      variable (y). ynodes need not be equally spaced.
      If ynodes is a scalar integer, then it specifies the number
      of equally spaced nodes between the min and max of the data.
      Also see the extend property.

    Returns
    -------
    zgrid: a numpy array of shape (nx,ny) containing the fitted surface
    xgrid, ygrid: as returned by meshgrid(xnodes,ynodes)


    Note
    ----
    Remember that gridfit must solve a LARGE system of linear
    equations. There will be as many unknowns as the total
    number of nodes in the final lattice. While these equations
    may be sparse, solving a system of 10000 equations may take
    a second or so. Very large problems may benefit from the
    iterative solvers or from tiling.

    Examples
    --------
    >>> x = np.random.rand(100)
    >>> y = np.random.rand(100,)
    >>> z = np.exp(x+2*y)
    >>> xnodes = np.arange(0, 1, .1)
    >>> ynodes = np.arange(0, 1, .1)
    >>> zgrid, xgrid, ygrid = gridfit(x, y, z, xnodes, ynodes)
    """
    params = Params(**kwargs)

    # ensure all of x,y,z,xnodes,ynodes are column vectors,
    # also drop any NaN data
    x = x.ravel()
    y = y.ravel()
    z = z.ravel()
    k = np.logical_or.reduce([np.isnan(x), np.isnan(y), np.isnan(z)])
    x = x[np.logical_not(k)]
    y = y[np.logical_not(k)]
    z = z[np.logical_not(k)]
    xmin = np.min(x)
    xmax = np.max(x)
    ymin = np.min(y)
    ymax = np.max(y)

    # did they supply a scalar for the nodes?
    if len(xnodes) == 1:
        xnodes = np.linspace(xmin, xmax, xnodes)
        xnodes[-1] = xmax  # make sure it hits the max
    if len(ynodes) == 1:
        ynodes = np.linspace(ymin, ymax, ynodes)
        ynodes[-1] = ymax  # make sure it hits the max

    xnodes = xnodes.ravel()
    ynodes = ynodes.ravel()
    dx = np.diff(xnodes)
    dy = np.diff(ynodes)
    nx = len(xnodes)
    ny = len(ynodes)
    ngrid = nx * ny

    # set the scaling if autoscale was on
    if params.autoscale:
        params.xscale = np.mean(dx)
        params.yscale = np.mean(dy)
        # params.autoscale = 'off'

    # check to see if any tiling is necessary
    if params.tilesize < max(nx, ny):
        # split it into smaller tiles. compute zgrid and ygrid
        # at the very end if requested
        zgrid = tiled_gridfit(x, y, z, xnodes, ynodes, params)

    # its a single tile.

    # mask must be either an empty array, or a boolean
    # aray of the same size as the final grid.
    if params.mask is not None:
        nmask = params.mask.shape
        if len(params.mask) > 0 and ((nmask[1] != nx) or (nmask[0] != ny)):
            if (nmask(2) == ny) or (nmask(1) == nx):
                raise ValueError(
                    "Mask array is probably transposed from proper orientation."
                )
            else:
                raise ValueError("Mask array must be the same size as the final grid.")

    # default for maxiter?
    if params.maxiter is None:
        params.maxiter = min(10000, nx * ny)

    # check lengths of the data
    n = len(x)
    if (len(y) != n) or (len(z) != n):
        raise Exception("Data vectors are incompatible in size.")

    if n < 3:
        raise Exception("Insufficient data for surface estimation.")

    # verify the nodes are distinct
    if np.any(np.diff(xnodes) <= 0) or np.any(np.diff(ynodes) <= 0):
        raise Exception("xnodes and ynodes must be monotone increasing")

    # do we need to tweak the first or last node in x or y?
    if xmin < xnodes[0]:
        if params.extend == "always":
            xnodes[0] = xmin
        elif params.extend == "warning":
            warn(
                f"GRIDFIT:extend, {xnodes[0]} was decreased by: '{xnodes[0]-xmin}', new node = '{xmin}"
            )
            xnodes[0] = xmin
        elif params.extend == "never":
            raise Exception(
                f"Some x ({xmin}) falls below {xnodes[0]} by: '{xnodes[0]-xmin}'"
            )
        else:
            pass  # TODO: Check this

    if xmax > xnodes[-1]:
        if params.extend == "always":
            xnodes[-1] = xmax
        elif params.extend == "warning":
            warn(
                f"GRIDFIT:extend xnodes[-1] was increased by {xmax-xnodes[-1]}, new node = {xmax}"
            )
            xnodes[-1] = xmax
        elif params.extend == "never":
            raise Exception(
                f"Some x ({xmax}) falls above xnodes[-1] by: {xmax-xnodes[-1]}"
            )
        else:
            pass  # TODO: Check this

    if ymin < ynodes[0]:
        if params.extend == "always":
            ynodes[0] = ymin
        elif params.extend == "warning":
            warn(
                f"GRIDFIT:extend ynodes[0] was decreased by {ynodes[0]-ymin}, new node = {ymin}"
            )
            ynodes[0] = ymin
        elif params.extend == "never":
            raise Exception(
                f"Some y ({ymin}) falls below ynodes[0] by: {ynodes[0]-ymin}"
            )
        else:
            pass
    if ymax > ynodes[-1]:
        if params.extend == "always":
            ynodes[-1] = ymax
        elif params.extend == "warning":
            warn(
                f"GRIDFIT:extend ynodes[-1] was increased by: {ymax-ynodes[-1]}, new node = {ymax}"
            )
            ynodes[-1] = ymax
        elif params.extend == "never":
            raise Exception(
                f"Some y ({ymax}) falls above ynodes[-1] by: {ymax-ynodes[-1]}"
            )
        else:
            pass

    # determine which cell in the array each point lies in
    # any point falling out of range is forced into the nearest tile
    indx = np.clip(np.digitize(x, xnodes), 1, nx - 1)
    indy = np.clip(np.digitize(y, ynodes), 1, ny - 1)

    # change tile index to start from 0
    indx -= 1
    indy -= 1

    ind = indy + ny * indx

    # Do we have a mask to apply?
    if params.mask is not None:
        # if we do, then we need to ensure that every
        # cell with at least one data point also has at
        # least all of its corners unmasked.
        params.mask[ind] = 1
        params.mask[ind + 1] = 1
        params.mask[ind + ny] = 1
        params.mask[ind + ny + 1] = 1

    # interpolation equations for each point
    tx = np.clip((x - xnodes[indx]) / dx[indx], 0, 1)
    ty = np.clip((y - ynodes[indy]) / dy[indy], 0, 1)

    # Future enhancement: add cubic interpolant
    if params.interp == "triangle":
        # linear interpolation inside each triangle
        k = tx > ty
        L = np.ones((n,))
        L[k] = ny

        t1 = np.minimum(tx, ty)
        t2 = np.maximum(tx, ty)
        A = sparse.csr_array(
            (
                np.vstack([1 - t2, t1, t2 - t1]).T.ravel(),
                (
                    np.tile(np.arange(n)[:, None], (1, 3)).ravel(),
                    np.vstack([ind, ind + ny + 1, ind + L]).T.ravel(),
                ),
            ),
            shape=(n, ngrid),
        )

    elif params.interp == "nearest":
        # nearest neighbor interpolation in a cell
        k = round(1 - ty) + round(1 - tx) * ny
        A = sparse.csr_array((np.ones((n,)), (np.arange(n), ind + k)), shape=(n, ngrid))

    elif params.interp == "bilinear":
        # bilinear interpolation in a cell
        A = sparse.csr_array(
            (
                np.vstack(
                    [(1 - tx) * (1 - ty), (1 - tx) * ty, tx * (1 - ty), tx * ty]
                ).T.ravel(),
                (
                    np.tile(np.arange(n)[:, None], (1, 4)).ravel(),
                    np.vstack([ind, ind + 1, ind + ny, ind + ny + 1]).T.ravel(),
                ),
            ),
            shape=(n, ngrid),
        )
    else:
        pass  # TODO: check this
    rhs = z

    # do we have relative smoothing parameters?
    if np.isscalar(params.smoothness) == 1:
        # it was scalar, so treat both dimensions equally
        smoothparam = params.smoothness
        xyRelativeStiffness = [1, 1]
    else:
        # It was a vector, so anisotropy reigns.
        # I've already checked that the vector was of length 2
        smoothparam = np.sqrt(np.prod(params.smoothness))
        xyRelativeStiffness = params.smoothness.ravel() / smoothparam

    # Build regularizer. Add del^4 regularizer one day.
    if params.regularizer == "springs":
        # zero "rest length" springs
        i, j = np.meshgrid(np.arange(1, nx + 1), np.arange(np.arange(1, (ny - 1) + 1)))
        ind = j.ravel() + ny * (i.ravel() - 1)
        m = nx * (ny - 1)
        stiffness = 1 / (dy / params.yscale)
        Areg = sparse(
            np.tile(np.arange(1, m + 1), (1, 2)),
            [ind, ind + 1],
            xyRelativeStiffness(2) * stiffness(j.ravel()) * [-1, 1],
            m,
            ngrid,
        )

        i, j = np.meshgrid(np.arange(1, (nx - 1) + 1), np.arange(1, ny + 1))
        ind = j.ravel() + ny * (i.ravel() - 1)
        m = (nx - 1) * ny
        stiffness = 1.0 / (dx / params.xscale)
        Areg = [
            Areg,
            sparse(
                np.tile(np.arange(1, m + 1), (1, 2)),
                [ind, ind + ny],
                xyRelativeStiffness[0] * stiffness[i.ravel()] * [-1, 1],
                m,
                ngrid,
            ),
        ]

        i, j = np.meshgrid(np.arange(1, (nx - 1) + 1), np.arange(1, (ny - 1) + 1))
        ind = j.ravel() + ny * (i.ravel() - 1)
        m = (nx - 1) * (ny - 1)
        stiffness = 1.0 / np.sqrt(
            (dx[i.ravel()] / params.xscale / xyRelativeStiffness[0]) ** 2
            + (dy[j.ravel()] / params.yscale / xyRelativeStiffness[1]) ** 2
        )

        Areg = [
            Areg,
            sparse(
                np.tile(np.arange(1, m + 1), (1, 2)),
                [ind, ind + ny + 1],
                stiffness * [-1, 1],
                m,
                ngrid,
            ),
        ]

        Areg = [
            Areg,
            sparse(
                np.tile(np.arange(1, m + 1), (1, 2)),
                [ind + 1, ind + ny],
                stiffness * [-1, 1],
                m,
                ngrid,
            ),
        ]

    elif params.regularizer in ["diffusion", "laplacian"]:
        # thermal diffusion using Laplacian (del^2)
        i, j = np.meshgrid(np.arange(1, nx + 1), np.arange(2, (ny - 1) + 1))
        ind = j.ravel() + ny * (i.ravel() - 1)
        dy1 = dy(j.ravel() - 1) / params.yscale
        dy2 = dy(j.ravel()) / params.yscale

        Areg = sparse.csr_array(
            xyRelativeStiffness[1] * np.vstack([
                -2.0 / (dy1 * (dy1 + dy2)),
                2.0 / (dy1 * dy2),
                -2.0 / (dy2 * (dy1 + dy2)),
            ]).T.ravel(),
            (
                np.tile(ind[:,None], (1, 3)).ravel(),
                np.vstack([ind - 1, ind, ind + 1]).T.ravel(),
            ),
            shape = (ngrid, ngrid)
        )

        i, j = np.meshgrid(np.arange(2, (nx - 1) + 1), np.arange(1, ny + 1))
        ind = j.ravel() + ny * (i.ravel() - 1)
        dx1 = dx(i.ravel() - 1) / params.xscale
        dx2 = dx(i.ravel()) / params.xscale

        Areg = Areg + sparse.csr_array(
            xyRelativeStiffness(1) * np.vstack([
                -2.0 / (dx1 * (dx1 + dx2)),
                2.0 / (dx1 * dx2),
                -2.0 / (dx2 * (dx1 + dx2)),
            ]).T.ravel(),
            (
                np.tile(ind[:, None], (1, 3)).ravel(),
                np.vstack([ind - ny, ind, ind + ny]).T.ravel(),
            ),
            shape = (ngrid, ngrid)
        )

    elif params.regularizer == "gradient":
        # Subtly different from the Laplacian. A point for future
        # enhancement is to do it better for the triangle interpolation
        # case.
        i, j = np.meshgrid(np.arange(nx), np.arange(1, (ny - 1)))
        ind = j.ravel() + ny * i.ravel()
        dy1 = dy[j.ravel() - 1] / params.yscale
        dy2 = dy[j.ravel()] / params.yscale

        Areg = sparse.csr_array(
            (
                xyRelativeStiffness[1]
                * np.vstack(
                    [
                        -2.0 / (dy1 * (dy1 + dy2)),
                        2.0 / (dy1 * dy2),
                        -2.0 / (dy2 * (dy1 + dy2)),
                    ]
                ).T.ravel(),
                (
                    np.tile(ind[:, None], (1, 3)).ravel(),
                    np.vstack([ind - 1, ind, ind + 1]).T.ravel(),
                ),
            ),
            shape=(ngrid, ngrid),
        )

        i, j = np.meshgrid(np.arange(1, (nx - 1)), np.arange(ny))
        ind = j.ravel() + ny * i.ravel()
        dx1 = dx[i.ravel() - 1] / params.xscale
        dx2 = dx[i.ravel()] / params.xscale

        Areg = sparse.vstack(
            [
                Areg,
                sparse.csr_array(
                    (
                        xyRelativeStiffness[0]
                        * np.vstack(
                            [
                                -2.0 / (dx1 * (dx1 + dx2)),
                                2.0 / (dx1 * dx2),
                                -2.0 / (dx2 * (dx1 + dx2)),
                            ]
                        ).T.ravel(),
                        (
                            np.tile(ind[:, None], (1, 3)).ravel(),
                            np.vstack([ind - ny, ind, ind + ny]).T.ravel(),
                        ),
                    ),
                    shape=(ngrid, ngrid),
                ),
            ]
        )

    nreg = Areg.shape[0]

    # Append the regularizer to the interpolation equations,
    # scaling the problem first. Use the 1-norm for speed.
    try:
        NA = sparse.linalg.norm(A, ord=1)
        NR = sparse.linalg.norm(Areg, ord=1)
    except np.AxisError:  # This is a bug in scipy sparse linalg for norm on sparse array
        NA = np.linalg.norm(A.toarray(), ord=1)
        NR = np.linalg.norm(Areg.toarray(), ord=1)
    A = sparse.vstack([A, Areg * (smoothparam * NA / NR)])
    rhs = np.hstack([rhs, np.zeros((nreg,))])
    # do we have a mask to apply?
    if params.mask is not None:
        (unmasked,) = np.where(params.mask)

    # solve the full system, with regularizer attached
    if params.solver in ["backslash", "normal"] and not (A.shape[0] == A.shape[1]):
        warn(
            "Scipy's sparse linalg solver 'spsolve' only supports square matrix. Using lsqr instead."
        )
        params.solver = "lsqr"

    if params.solver == "backslash":
        if params.mask is not None:
            # there is a mask to use
            zgrid = np.full((ny, nx), np.nan)
            zgrid[unmasked] = scipy.linalg.solve(A[:, unmasked], rhs)
        else:
            # no mask
            zgrid = sparse.linalg.spsolve(A, rhs).reshape((ny, nx), order="F")

    elif params.solver == "normal":
        # The normal equations, solved with \. Can be faster
        # for huge numbers of data points, but reasonably
        # sized grids. The regularizer makes A well conditioned
        # so the normal equations are not a terribly bad thing
        # here.
        if params.mask is not None:
            # there is a mask to use
            Aunmasked = A[:, unmasked]
            zgrid = np.full((ny, nx), np.nan)
            zgrid[unmasked] = sparse.linalg.solve(
                (Aunmasked.T @ Aunmasked), (Aunmasked.T @ rhs)
            )
        else:
            zgrid = scipy.linalg.solve((A.T @ A), (A.T @ rhs)).reshape(
                (ny, nx), order="F"
            )

    elif params.solver == "lsqr":
        # iterative solver - lsqr. No preconditioner here.
        tol = np.abs(np.max(z) - np.min(z)) * 1.0e-13
        if params.mask is not None:
            # there is a mask to use
            zgrid = np.full((ny, nx), np.nan)
            zgrid[unmasked] = sparse.linalg.lsqr(
                A[:, unmasked], rhs, atol=tol, iter_lim=params.maxiter
            )[0]
        else:
            zgrid = sparse.linalg.lsqr(A, rhs, atol=tol, iter_lim=params.maxiter)[0]
            zgrid = zgrid.reshape((ny, nx), order="F")

    # only generate xgrid and ygrid if requested.
    xgrid, ygrid = np.meshgrid(xnodes, ynodes)

    return zgrid, xgrid, ygrid


def tiled_gridfit(x, y, z, xnodes, ynodes, params: Params):
    """A tiled version of gridfit, continuous across tile boundaries

    Tiled_gridfit is used when the total grid is far too large
    to model using a single call to gridfit. While gridfit may take
    only a second or so to build a 100x100 grid, a 2000x2000 grid
    will probably not run at all due to memory problems.

    Tiles in the grid with insufficient data (<4 points) will be
    filled with NaNs. Avoid use of too small tiles, especially
    if your data has holes in it that may encompass an entire tile.

    A mask may also be applied, in which case tiled_gridfit will
    subdivide the mask into tiles. Note that any boolean mask
    provided is assumed to be the size of the complete grid.

    Tiled_gridfit may not be fast on huge grids, but it should run
    as long as you use a reasonable tilesize. 8-)
    """
    # Matrix elements in a square tile
    tilesize = params.tilesize
    # Size of overlap in terms of matrix elements. Overlaps
    # of purely zero cause problems, so force at least two
    # elements to overlap.
    overlap = max(2, np.floor(tilesize * params.overlap))

    # reset the tilesize for each particular tile to be inf, so
    # we will never see a recursive call to tiled_gridfit
    Tparams = params
    Tparams.tilesize = np.inf

    nx = len(xnodes)
    ny = len(ynodes)
    zgrid = np.zeros((ny, nx))

    # linear ramp for the bilinear interpolation
    rampfun = lambda t: (t - t[0]) / (t[-1] - t[0])

    # loop over each tile in the grid
    wbar = tqdm(desc="Relax and have a cup of JAVA. Its my treat.")
    warncount = 0
    xtind = np.arange(1, min(nx, tilesize) + 1)
    while len(xtind) > 0 and (xtind[0] <= nx):

        xinterp = np.ones((len(xtind),))
        if xtind[0] != 1:
            xinterp[:overlap] = rampfun(xnodes[xtind[:overlap]])
        if xtind[-1] != nx:
            xinterp[(-overlap + 1) :] = 1 - rampfun(xnodes[xtind[(-overlap + 1) :]])

        ytind = np.arange(1, min(ny, tilesize))
        while len(ytind) > 0 and (ytind[0] <= ny):
            # update the waitbar
            _step = (xtind[-1] - tilesize) / nx + tilesize * ytind[-1] / ny / nx
            wbar.n = _step
            wbar.last_print_n = _step

            yinterp = np.ones((len(ytind),))
            if ytind[0] != 1:
                yinterp[:overlap] = rampfun(ynodes[ytind[:overlap]])
            if ytind[-1] != ny:
                yinterp[-overlap + 1 :] = 1 - rampfun(ynodes[ytind[-overlap + 1 :]])

            # was a mask supplied?
            if len(params.mask) > 0:
                submask = params.mask[ytind, xtind]
                Tparams.mask = submask

            # extract data that lies in this grid tile
            k = np.logical_and.reduce(
                [
                    x >= xnodes[xtind[0]],
                    x <= xnodes[xtind[-1]],
                    y >= ynodes[ytind[0]],
                    y <= ynodes[ytind[-1]],
                ]
            )
            (k,) = np.where(k)

            if len(k) < 4:
                if warncount == 0:
                    warn(
                        "GRIDFIT:tiling A tile was too underpopulated to model. Filled with NaNs."
                    )
                warncount += 1

                # fill this part of the grid with NaNs
                zgrid[ytind, xtind] = np.nan

            else:
                # build this tile
                zgtile = gridfit(
                    x[k], y[k], z[k], xnodes[xtind], ynodes[ytind], Tparams
                )

                # bilinear interpolation (using an outer product)
                interp_coef = yinterp * xinterp

                # accumulate the tile into the complete grid
                zgrid[ytind, xtind] += zgtile * interp_coef

            # step to the next tile in y
            if ytind[-1] < ny:
                ytind += tilesize - overlap
                # are we within overlap elements of the edge of the grid?
                if (ytind[-1] + max(3, overlap)) >= ny:
                    # extend this tile to the edge
                    ytind = np.arange(ytind[0], ny + 1)
            else:
                ytind = ny + 1

        # step to the next tile in x
        if xtind[-1] < nx:
            xtind = xtind + tilesize - overlap
            # are we within overlap elements of the edge of the grid?
            if (xtind[-1] + max(3, overlap)) >= nx:
                # extend this tile to the edge
                xtind = np.arange(xtind[0], nx + 1)
        else:
            xtind = nx + 1

    # close down the waitbar
    wbar.close()

    if warncount > 0:
        warn(f"GRIDFIT:tiling:{warncount} tiles were underpopulated & filled with NaNs")
    return zgrid
