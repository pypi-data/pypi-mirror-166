
import numpy as np
from scipy.io import loadmat
from gridfit import gridfit
from pathlib import Path
import matplotlib
matplotlib.use('macosx')
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

# Topographic data
TEST_DIR = Path(__file__).parent.resolve()
bluff_data = loadmat(TEST_DIR / 'bluff_data.mat')
x, y, z = bluff_data['bluff_data'].astype(np.float_).T

# Turn the scanned point data into a surface
gx=np.arange(0, 264+1, 4)
gy=np.arange(0, 400+1, 4)
g, XX, YY =gridfit(x,y,z,gx,gy)


fig,ax = plt.subplots(1,1, subplot_kw=dict(projection='3d'))
ls = LightSource(azdeg=0, altdeg=65)
rgb = ls.shade(g, plt.cm.hot)
ax.plot_surface(
    XX,YY,g,
    rstride=1, cstride=1, linewidth=0,
    antialiased=False, facecolors=rgb
)
ax.plot(x,y,z,'.',markersize=4)
ax.set_title('Use topographic contours to recreate a surface')
plt.show()