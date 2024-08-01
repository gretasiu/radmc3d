#
# Importing files and packages
#
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import central_star as cs
#
# Some natural constants
#
au = 1.49598e13     # Astronomical Unit       [cm]
pc = 3.08572e18     # Parsec                  [cm]
ms = 1.98892e33     # Solar mass              [g]
Ts = 5.78e3         # Solar temperature       [K]
Ls = 3.8525e33      # Solar luminosity        [erg/s]
Rs = 6.96e10        # Solar radius            [cm]
m_H = 1.6736e-24    # mass of one H atom      [g]
gas_to_dust_ratio = 100
#
# Number of photons
#
nphot = 1e7
nphot_scat = 1e7
#
# Grid parameters
#
nx = 100  # number of cell on x axis; number of cell scaling with the values from exmaple
ny = 100
nz = 100
sizex = 2e4*au  # 2e4 au is the length of the line drawn to extract the 1D intensity profile
sizey = 2e4*au
sizez = 2e4*au

#
# Density model parameters (taken from eqn 2 and table 6 from Yuxin Lin 2022)
#
rhoc = 29.9e5*(2.8*m_H)/gas_to_dust_ratio  # g cm^-3
rc = 0.1*pc
n = 1.22
#
# Star parameters
#
mstar = cs.M_star_G31*ms
rstar = cs.R_star_G31*Rs
tstar = cs.T_star_G31
pstar = np.array([0., 0., 0.])  # posiiton of the star inside the grid; center
#
# Make the coordinates for density profile
#
xi = np.linspace(-sizex, sizex, nx+1)  # finding all the walls of the cells
yi = np.linspace(-sizey, sizey, nx+1)
zi = np.linspace(-sizez, sizez, nx+1)
# finding the midpoints of each cell by adding up walls from both sides and dividing by 2
xc = 0.5 * (xi[0:nx] + xi[1:nx+1])
yc = 0.5 * (yi[0:ny] + yi[1:ny+1])
zc = 0.5 * (zi[0:nz] + zi[1:nz+1])
#
# Dust density model
#
qq = np.meshgrid(xc, yc, zc, indexing='ij')
xx = qq[0]
yy = qq[1]
zz = qq[2]
rr = np.sqrt(xx**2+yy**2+zz**2)
rhod = rhoc*(rr/rc)**(-n)
# print(xx)
#
# wavelength which I want to calculate over
#
lammin = 1e-10
lammax = 1e4
steplam = 1000
lam = np.logspace(np.log10(lammin), np.log10(lammax), steplam)
nlam = lam.size
#
# Now the alignment vector field. This is ONLY FOR TESTING.
#
alvec = np.zeros((nx, ny, nz, 3))
scaling = sizex/'scaling_PLACEHOLDER'
x, y, z = xx/scaling, yy/scaling, zz/scaling

# input code for B field: start
r = np.sqrt(x**2 + y**2)
s = r/z
v0 = 'pitchness_PLACEHOLDER'
w = np.sqrt(r**2 + z**2)
p = 2
v = 1 + v0*(1+w**2)**(-p/2)
avg_v = 1 + ((3*v0)/(w**2))*(1 - (np.arctan(w))/(w))
t = v/avg_v
theta_B = np.arctan((1-t)/(s*((s**-2)+t)))
mask = (x == 0) & (y == 0)
theta_B[mask] = 0
Bz = np.cos(theta_B)
Bxy = np.sin(theta_B)
# angles on x-y plane
phi = np.arctan(y/x)
phi[y == 0] = 0
phi[x == 0] = np.pi/2
Bx = Bxy*np.cos(phi)
By = Bxy*np.sin(phi)
# manipulation by hand
Bx[x < 0] = -Bx[x < 0]
By[x < 0] = -By[x < 0]
mask = (x == 0) & (y < 0)
By[mask] = -By[mask]

# Normalizing the B vectors
norm = np.sqrt(Bx**2 + By**2 +Bz**2)
Bx = Bx/norm 
By = By/norm
Bz = Bz/norm

# torodial field (Stefan Reissl thesis)
Bk = 'rotation_per_PLACEHOLDER'
rotation_power = 'rotation_power_PLACEHOLDER'
const = Bk/(np.sqrt(x**2 + y**2))**rotation_power
Bx_toro = const*y
By_toro = const*-x
Bz_toro = 0

# combining poloidial and torodial
Bx_pt = Bx + Bx_toro
By_pt = By + By_toro
Bz_pt = Bz + Bz_toro
# input code for B field: end

# Putting B vector from our model into the proper array
alvec[:, :, :, 0] = Bx_pt
alvec[:, :, :, 1] = By_pt
alvec[:, :, :, 2] = Bz_pt
#
# Normalize
#
length = np.sqrt(alvec[:, :, :, 0]*alvec[:, :, :, 0]+alvec[:, :, :, 1]
                 * alvec[:, :, :, 1]+alvec[:, :, :, 2]*alvec[:, :, :, 2])
alvec[:, :, :, 0] = np.squeeze(alvec[:, :, :, 0]) / (length + 1e-60)
alvec[:, :, :, 1] = np.squeeze(alvec[:, :, :, 1]) / (length + 1e-60)
alvec[:, :, :, 2] = np.squeeze(alvec[:, :, :, 2]) / (length + 1e-60)

# Now include the alignment efficiency.
# Setting a constant aligment efficiency

epsal = 1
alvec[:, :, :, 0] = np.squeeze(alvec[:, :, :, 0]) * epsal
alvec[:, :, :, 1] = np.squeeze(alvec[:, :, :, 1]) * epsal
alvec[:, :, :, 2] = np.squeeze(alvec[:, :, :, 2]) * epsal

# #
# # Plot B field on 2D quiver plot
# #
# xplot, zplot = np.meshgrid(np.linspace(-sizex, sizex, 50), np.linspace(-sizez, sizez, 50))
# x, z = xplot/scaling, zplot/scaling
# s = x/z
# w = np.sqrt(x**2 + z**2)
# p = 2
# v = 1 + v0*(1+w**2)**(-p/2)
# avg_v = 1 + ((3*v0)/(w**2))*(1 - (np.arctan(w))/(w))
# t = v/avg_v
# theta_B = np.arctan((1-t)/(s*((s**-2)+t)))
# # theta_B[x == 0] = 0
# Bx = np.sin(theta_B)
# Bz = np.cos(theta_B)
# fig = plt.figure(figsize=(8,8))
# ax = fig.gca()
# ax.quiver(xplot, zplot, Bx, Bz, headaxislength=0, headlength=0)
# ax.set_xlabel('x')
# ax.set_ylabel('z')
# fig.savefig('fig/Bfield_vectorPlot.pdf')

# Write the wavelength_micron.inp file
#
with open('wavelength_micron.inp', 'w+') as f:
    f.write('%d\n' % (nlam))
    for value in lam:
        f.write('%13.6e\n' % (value))
#
# write the star.inp file
#
with open('stars.inp', 'w+') as f:
    f.write('2\n')
    f.write('1 %d\n\n' % (nlam))
    f.write('%13.6e %13.6e %13.6e %13.6e %13.6e\n\n' %
            (rstar, mstar, pstar[0], pstar[1], pstar[2]))
    for value in lam:
        f.write('%13.6e\n' % (value))
    f.write('\n%13.6e\n' % (-tstar))
#
# Write the grid file
#
with open('amr_grid.inp', 'w+') as f:
    f.write('1\n')                       # iformat
    # AMR grid style  (0=regular grid, no AMR)
    f.write('0\n')
    f.write('0\n')                       # Coordinate system
    f.write('0\n')                       # gridinfo
    f.write('1 1 1\n')                   # Include x,y,z coordinate
    f.write('%d %d %d\n' % (nx, ny, nz))     # Size of grid
    for value in xi:
        f.write('%13.6e\n' % (value))      # X coordinates (cell walls)
    for value in yi:
        f.write('%13.6e\n' % (value))      # Y coordinates (cell walls)
    for value in zi:
        f.write('%13.6e\n' % (value))      # Z coordinates (cell walls)
#
# Write the density file
#
with open('dust_density.inp', 'w+') as f:
    f.write('1\n')                       # Format number
    f.write('%d\n' % (nx*ny*nz))           # Nr of cells
    f.write('1\n')                       # Nr of dust species
    # Create a 1-D view, fortran-style indexing
    data = rhod.ravel(order='F')
    data.tofile(f, sep='\n', format="%13.6e")
    f.write('\n')
#
# Dust opacity control file
#
with open('dustopac.inp', 'w+') as f:
    f.write('2               Format number of this file\n')
    f.write('1               Nr of dust species\n')
    f.write(
        '============================================================================\n')
    f.write('20               Way in which this dust species is read\n')
    f.write('0               0=Thermal grain\n')
    f.write('s-a10um        Extension of name of dustkappa_***.inp file\n')
    f.write(
        '----------------------------------------------------------------------------\n')
#
# Dust alignment direction
#
with open('grainalign_dir.inp', 'w+') as f:
    f.write('1\n')                       # Format number
    f.write('%d\n' % (nx*ny*nz))           # Nr of cells
    for iz in range(nz):
        for iy in range(ny):
            for ix in range(nx):
                f.write('%13.6e %13.6e %13.6e\n' % (
                    alvec[ix, iy, iz, 0], alvec[ix, iy, iz, 1], alvec[ix, iy, iz, 2]))
#
# Write the radmc3d.inp control file
#
with open('radmc3d.inp', 'w+') as f:
    f.write('nphot = %d\n' % (nphot))
    f.write('nphot_scat = %d\n' % (nphot_scat))
    f.write('scattering_mode_max = 4\n')
    f.write('alignment_mode = 1\n')
    f.write('setthreads = 20\n')
    f.write('istar_sphere = 0\n')
    f.write('modified_random_walk = 1\n')
    f.write('mc_scat_maxtauabs = 10\n')
