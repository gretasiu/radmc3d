import numpy as np
import setup as p
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d
from matplotlib import pyplot as plt
from matplotlib import cm
from radmc3dPy.image import *
from radmc3dPy.analyze import *
from plotpoldir import *
import math
au = 1.49598e13     # Astronomical Unit       [cm]

# global parameters suitable for both wavelength
npix = 'npix_PLACEHOLDER'  # on each of x and y axis. so the total number of pixel is 1000^2
incl = 'incl_PLACEHOLDER'
phi = 'phi_PLACEHOLDER'
posang = 'posang_PLACEHOLDER'
sizeau1300 = 'sizeau1300_PLACEHOLDER'
sizeau7000 = 'sizeau7000_PLACEHOLDER'
Bfield = False

# #
# # Plot the opacity table
# #
# o = readOpac(ext='sg-a10um')
# plt.figure()
# plt.loglog(o.wav[0], o.kabs[0],
#            label=r'$\kappa_\nu^{\mathrm{abs}}$ (absorption)')
# plt.loglog(o.wav[0], o.ksca[0], ':',
#            label=r'$\kappa_\nu^{\mathrm{scat}}$ (scattering)')
# plt.ylim((1e-2, 1e5))
# plt.xlabel(r'$\lambda\;[\mu\mathrm{m}]$')
# plt.ylabel(r'$\kappa_\nu\;[\mathrm{cm}^2/\mathrm{g}]$')
# plt.title(r'Dust opacity ($a_{max}=10\,\mu\mathrm{m}$)')
# plt.legend()
#
# Make and plot an example image
#
# # 1.3mm imaging
makeImage(npix=npix, incl=incl, phi=phi, posang=posang, wav=1300,
          sizeau=sizeau1300)   # This calls radmc3d
fig2 = plt.figure()
a = readImage()
#plotImage(a, cmap=cm.hot, au=True, bunit='inu', ifreq=0)
# plotpoldir(a.x/au, a.y/au, a.image[:, :, 0, 0],
#            a.image[:, :, 1, 0], a.image[:, :, 2, 0], Bfield=Bfield)
a.writeFits('radmc3d_1300_I.fits', dpc=3750., stokes='I')
a.writeFits('radmc3d_1300_Q.fits', dpc=3750., stokes='Q')
a.writeFits('radmc3d_1300_U.fits', dpc=3750., stokes='U')

# 7mm imaging
makeImage(npix=npix, incl=incl, phi=phi, posang=posang, wav=7000,
          sizeau=sizeau7000)   # This calls radmc3d
fig2 = plt.figure()
a = readImage()
#plotImage(a, cmap=cm.hot, au=True, bunit='inu', ifreq=0)
# plotpoldir(a.x/au, a.y/au, a.image[:, :, 0, 0],
#            a.image[:, :, 1, 0], a.image[:, :, 2, 0], Bfield=Bfield)
a.writeFits('radmc3d_7000_I.fits', dpc=3750., stokes='I')
a.writeFits('radmc3d_7000_Q.fits', dpc=3750., stokes='Q')
a.writeFits('radmc3d_7000_U.fits', dpc=3750., stokes='U')

#
# Use the radmc3dPy.analyze tool set to read in the dust temperatures
# calculated by the command-line command "radmc3d mctherm"
#
# q = readData()
# fig5 = plt.figure()
# fig6 = plt.figure()
# ay5 = fig5.gca(projection='3d')
# ay6 = fig6.gca()
# qq = np.meshgrid(q.grid.x, q.grid.y, q.grid.z, indexing='ij')
# xx = qq[0][:, :, 50]
# yy = qq[1][:, :, 50]
# # The extra "0" is because of possible multiple dust species; here only 1 dust species
# dd = q.dusttemp[:, :, 50, 0]
# ay5.plot_surface(xx, yy, dd, rstride=1, cstride=1,
#                  cmap=cm.coolwarm, linewidth=1)
# c = ay6.pcolor(xx, yy, dd, cmap=cm.coolwarm, linewidth=1, shading='auto')
# fig6.colorbar(c, label='[K]')


plt.show()
