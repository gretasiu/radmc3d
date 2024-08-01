# Setup based on Sadavoy et al. (2018b)
# This is a modified script for the ALMA 1.3mm observation
# For the original version, this see Joaquin's script
# Antenna configuration provided in CASA: https://casaguides.nrao.edu/index.php?title=Antenna_Configurations_Models_in_CASA_Cycle5
# To execute them, just keep the script in the folder containing the fitsfiles and run $ casa -c alma_polarization_simulation.py

import time
import random

polarization = True

start = time.time()

# parameters for both synthetic observation and cleaning
antenna = 'alma.cycle4.5'

# getting rms information from dirty map
with open('rms_alma.txt', 'r') as file:
    lines = file.readlines()
    
rms_I = lines[0].strip()
rms_QU = lines[1].strip()
thresholdI = str(3*rms_I)
thresholdQU = str(3*rms_QU)

# paramters for cleaning
vis = antenna+'.noisy.ms'
imsize = 1776        # No. of size on in each axis
cell = '0.0242arcsec'
reffreq = '233GHz'
specmode = 'mfs'
gridder = 'standard'
deconvolver = 'hogbom'
weighting = 'natural'
# robust = 0.5                 # turn this on if weighting = 'briggs'
niter = 10000
# uvtaper='0.1arcsec'
# mask='centerbox[[200pix, 200pix], [50pix, 50pix]]'
threshold_I = thresholdI+'Jy'
threshold_QU = thresholdI+'Jy'
pbcor = True
interactive = False
verbose = True


print('\033[1m\n[alma_simulation] Cleaning Stokes I ...\033[0m')
tclean(
    vis='band6_I/band6_I.'+vis,
    imagename='band6_I/clean_I',
    imsize=imsize,
    cell=cell,
    reffreq=reffreq,
    specmode=specmode,
    gridder=gridder,
    deconvolver=deconvolver,
    weighting=weighting,
    niter=niter,
    threshold=threshold_I,
    pbcor=pbcor,
    interactive=interactive,
    verbose=verbose
)
if polarization:
    print('\033[1m\n[alma_simulation] Cleaning Stokes Q ...\033[0m')
    tclean(
        vis='band6_Q/band6_Q.'+vis,
        imagename='band6_Q/clean_Q',
        imsize=imsize,
        cell=cell,
        reffreq=reffreq,
        specmode=specmode,
        gridder=gridder,
        deconvolver=deconvolver,
        weighting=weighting,
        niter=niter,
        threshold=threshold_QU,
        pbcor=pbcor,
        interactive=interactive,
        verbose=verbose
    )
    print('\033[1m\n[alma_simulation] Cleaning Stokes U ...\033[0m')
    tclean(
        vis='band6_U/band6_U.'+vis,
        imagename='band6_U/clean_U',
        imsize=imsize,
        cell=cell,
        reffreq=reffreq,
        specmode=specmode,
        gridder=gridder,
        deconvolver=deconvolver,
        weighting=weighting,
        niter=niter,
        threshold=threshold_QU,
        pbcor=pbcor,
        interactive=interactive,
        verbose=verbose
    )

# changed Jul 7 2024 -- regridding synobs to obs 
imregrid('band6_I/clean_I.image', template='realobs/G31_ALMAb6pol_I.dropdeg.image',
            output='band6_I/clean_I.image_modelsize', overwrite=True)
exportfits('band6_I/clean_I.image_modelsize',
            fitsimage='synobs_1300_I.fits', dropdeg=True, overwrite=True)
exportfits('band6_I/clean_I.image',
            fitsimage='band6_I/clean_I.fits', dropdeg=True, overwrite=True)


if polarization:
    # changed Jul 7 2024 -- regridding synobs to obs 
    imregrid('band6_Q/clean_Q.image', template='realobs/G31_ALMAb6pol_I.dropdeg.image',
                output='band6_Q/clean_Q.image_modelsize', overwrite=True)
    imregrid('band6_U/clean_U.image', template='realobs/G31_ALMAb6pol_I.dropdeg.image',
                output='band6_U/clean_U.image_modelsize', overwrite=True)
    exportfits('band6_Q/clean_Q.image_modelsize',
                fitsimage='synobs_1300_Q.fits', dropdeg=True, overwrite=True)
    exportfits('band6_Q/clean_Q.image',
                fitsimage='band6_Q/clean_Q.fits', dropdeg=True, overwrite=True)
    exportfits('band6_U/clean_U.image_modelsize',
                fitsimage='synobs_1300_U.fits', dropdeg=True, overwrite=True)
    exportfits('band6_U/clean_U.image',
                fitsimage='band6_U/clean_U.fits', dropdeg=True, overwrite=True)


print('\n[alma_simulaton] Elapsed time: {}'
      .format(time.strftime("%H:%M:%S", time.gmtime(time.time()-start)))
      )
