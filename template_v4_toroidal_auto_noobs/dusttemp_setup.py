import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from radmc3dPy.image import *
from radmc3dPy.analyze import *
import setup as su

#
# Some natural constants
#
au = 1.49598e13     # Astronomical Unit       [cm]
pc = 3.08572e18     # Parsec                  [cm]

# radius of G31 in Lin 2022
r = np.linspace(1e-2, 1, 100)

# parameters taken from table 5 and equ3.(3) of Lin 2022
Tin = 400  # [K]
Tout = 18.3  # [K]
rin = 0.01  # [pc]
rout = 0.21  # [pc]
w = np.exp(-r/rout)

# temperature profile (Lin 2022)
Temp = w*Tin*(r/rin)**(-0.5) + (1-w)*Tout

# plotting the temperature profile to make sure it looks the same as in fig 20 (Lin 2022)
# fig = plt.figure(figsize=(12, 9))
# plt.semilogx()
# plt.semilogy()
# plt.xlim(1e-2, 1)
# plt.ylim(3e0, 4e2)
# plt.title("G31.41+0.31 radial temperaure (Lin 2022 fig 20)")
# plt.xlabel("Radius [pc]")
# plt.ylabel("Temperature [K]")
# plt.plot(r, Temp)
# plt.savefig("fig/radialtemp_Lin2022.pdf")
# plt.show()
# plt.close(fig)

#
# Creating radmc3d dust_temperature.dat input file in 3D cartesean coordinate
#
# rewriting temperature profile in cartesean coordiante
Tin = 400  # [K]
Tout = 18.3  # [K]
rin = 0.01*pc  # [cm]
rout = 0.21*pc  # [cm]
w = np.exp(-su.rr/rout)
Temp = w*Tin*(su.rr/rin)**(-0.5) + (1-w)*Tout

# writing dust temperature to file using the format of dust density
with open('dust_temperature.dat', 'w+') as f:
    f.write('1\n')                       # Format number
    f.write('%d\n' % (su.nx*su.ny*su.nz))           # Nr of cells
    f.write('1\n')                       # Nr of dust species
    # Create a 1-D view, fortran-style indexing
    data = Temp.ravel(order='F')
    data.tofile(f, sep='\n', format="%13.6e")
    f.write('\n')
    data = Temp.ravel(order='F')
    data.tofile(f, sep='\n', format="%13.6e")
    f.write('\n')
    data = Temp.ravel(order='F')
    data.tofile(f, sep='\n', format="%13.6e")
    f.write('\n')
    data = Temp.ravel(order='F')
    data.tofile(f, sep='\n', format="%13.6e")
    f.write('\n')

# # plotting the 2D temperature map when slicing the cube in the middle along the XY plane
# q = readData()
# fig = plt.figure(figsize=(15, 12))
# ay = fig.gca()
# qq = np.meshgrid(q.grid.x, q.grid.y, q.grid.z, indexing='ij')
# xx = qq[0][:, :, su.nz/2]
# yy = qq[1][:, :, su.nz/2]
# # The extra "0" is because of possible multiple dust species; here only 1 dust species
# dd = q.dusttemp[:, :, su.nz/2, 0]
# c = ay.pcolor(xx, yy, dd, cmap=cm.coolwarm, linewidth=1, shading='auto')
# fig.colorbar(c, label='[K]')
# plt.savefig("fig/dust_temp_middleslice.png")
# plt.show()
# plt.close(fig)

# # plotting the temperature profile in the radius range comparable to the G31 model
# r = np.linspace(10*au, su.sizex, 100)
# Tin = 400  # [K]
# Tout = 18.3  # [K]
# rin = 0.01*pc  # [cm]
# rout = 0.21*pc  # [cm]
# w = np.exp(-r/rout)
# Temp = w*Tin*(r/rin)**(-0.5) + (1-w)*Tout

# fig = plt.figure(figsize=(12, 9))
# plt.semilogx()
# plt.semilogy()
# plt.title("G31.41+0.31 radial temperaure")
# plt.xlabel("Radius [cm]")
# plt.ylabel("Temperature [K]")
# plt.plot(r, Temp)
# plt.savefig("fig/radialtemp_modelsize.pdf")
# plt.show()
# plt.close(fig)
