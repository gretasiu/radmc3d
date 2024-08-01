# Setup based on Liu et al. (2018)
# Antenna configuration provided in CASA: https://casaguides.nrao.edu/index.php?title=Antenna_Configurations_Models_in_CASA_Cycle5
# To execute them, just keep the script in the folder containing the fitsfiles and run $ casa -c vla_polarization_simulation.py

import time
import random

polarization = True

start = time.time()

# parameters for both synthetic observation and cleaning
antenna = 'vla.d'

# getting rms information from dirty map
with open('rms_vla.txt', 'r') as file:
    lines = file.readlines()
    
rms_I = lines[0].strip()
rms_QU = lines[1].strip()
thresholdI = str(3*rms_I)
thresholdQU = str(3*rms_QU)

# paramters for cleaning
vis = antenna+'.noisy.ms'
imsize = 323        # No. of call on in each axis
cell = '0.3arcsec'
reffreq = '44GHz'
specmode = 'mfs'
gridder = 'standard'
deconvolver = 'hogbom'
weighting = 'briggs'
robust = 2                 # turn this on if weighting = 'briggs'
niter = 10000
# uvtaper='0.1arcsec'
# mask='centerbox[[200pix, 200pix], [50pix, 50pix]]'
threshold_I = thresholdI+'Jy'
threshold_QU = thresholdI+'Jy'
pbcor = True
interactive = False
verbose = True


print('\033[1m\n[vla_simulation] Cleaning Stokes I ...\033[0m')
tclean(
    vis='bandQ_I/bandQ_I.'+vis,
    imagename='bandQ_I/clean_I',
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
    print('\033[1m\n[vla_simulation] Cleaning Stokes Q ...\033[0m')
    tclean(
        vis='bandQ_Q/bandQ_Q.'+vis,
        imagename='bandQ_Q/clean_Q',
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
    print('\033[1m\n[vla_simulation] Cleaning Stokes U ...\033[0m')
    tclean(
        vis='bandQ_U/bandQ_U.'+vis,
        imagename='bandQ_U/clean_U',
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
imregrid('bandQ_I/clean_I.image', template='realobs/G31p4_Qband_D.rob2.I.image.tt0.image',
            output='bandQ_I/clean_I.image_modelsize', overwrite=True)
exportfits('bandQ_I/clean_I.image_modelsize',
            fitsimage='synobs_7000_I.fits', dropdeg=True, overwrite=True)
exportfits('bandQ_I/clean_I.image',
            fitsimage='bandQ_I/clean_I.fits', dropdeg=True, overwrite=True)

if polarization:
    # changed Jul 7 2024 -- regridding synobs to obs
    imregrid('bandQ_Q/clean_Q.image', template='realobs/G31p4_Qband_D.rob2.Q.image.tt0.image',
                output='bandQ_Q/clean_Q.image_modelsize', overwrite=True)
    imregrid('bandQ_U/clean_U.image', template='realobs/G31p4_Qband_D.rob2.U.image.tt0.image',
                output='bandQ_U/clean_U.image_modelsize', overwrite=True)
    exportfits('bandQ_Q/clean_Q.image_modelsize',
                fitsimage='synobs_7000_Q.fits', dropdeg=True, overwrite=True)
    exportfits('bandQ_Q/clean_Q.image',
                fitsimage='bandQ_Q/clean_Q.fits', dropdeg=True, overwrite=True)
    exportfits('bandQ_U/clean_U.image_modelsize',
                fitsimage='synobs_7000_U.fits', dropdeg=True, overwrite=True)
    exportfits('bandQ_U/clean_U.image',
                fitsimage='bandQ_U/clean_U.fits', dropdeg=True, overwrite=True)
    # added Jul 7 2024 -- regridding synobs to obs 
    
print('\n[vla_simulation] Elapsed time: {}'
    .format(time.strftime("%H:%M:%S", time.gmtime(time.time()-start)))
    )
