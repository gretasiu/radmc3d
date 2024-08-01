# Setup based on Sadavoy et al. (2018b)
# This is a modified script for the ALMA 1.3mm observation
# For the original version, this see Joaquin's script
# Antenna configuration provided in CASA: https://casaguides.nrao.edu/index.php?title=Antenna_Configurations_Models_in_CASA_Cycle5
# To execute them, just keep the script in the folder containing the fitsfiles and run $ casa -c alma_polarization_simulation.py

import time
import random

Simobserve = True
Dirty = True
polarization = True

start = time.time()

# parameters for both synthetic observation and cleaning
antenna = 'alma.cycle4.5'

# parameters for synthetic observation
source = 'radmc3d_1300'
incenter = '233GHz'
inwidth = '2GHz'
setpointings = True
integration = '2s'
totaltime = '1.235h'
indirection = 'J2000 18h47m34.308 -01d12m45.90'
refdate = '2017/07/12'
hourangle = 'transit'
obsmode = 'int'
antennalist = antenna+'.cfg'
thermalnoise = 'tsys-atm'
seed = int(random.random() * 100)
graphics = 'file'
overwrite = True
verbose = True

# paramters for cleaning
vis = antenna+'.noisy.ms'
imsize = 1776        # No. of cell on in each axis
cell = '0.0242arcsec'
reffreq = '233GHz'
specmode = 'mfs'
gridder = 'standard'
deconvolver = 'hogbom'
weighting = 'natural'
# robust = 0.5                 # turn this on if weighting = 'briggs'
niter = 0
# uvtaper='0.1arcsec'
# mask='centerbox[[200pix, 200pix], [50pix, 50pix]]'
threshold_I = '0.51Jy'
threshold_QU = '0.003Jy'
pbcor = True
interactive = False
verbose = True

if Simobserve:
    print('\033[1m\n[alma_simulation] Observing Stokes I ...\033[0m')
    simobserve(
        project='band6_I',
        skymodel=source+'_I.fits',
        incenter=incenter,
        inwidth=inwidth,
        setpointings=setpointings,
        integration=integration,
        totaltime=totaltime,
        indirection=indirection,
        refdate=refdate,
        hourangle=hourangle,
        obsmode=obsmode,
        antennalist=antennalist,
        thermalnoise=thermalnoise,
        seed=seed,
        graphics=graphics,
        overwrite=overwrite,
        verbose=verbose
    )
    if polarization:
        print('\033[1m\n[alma_simulation] Observing Stokes Q ...\033[0m')
        simobserve(
            project='band6_Q',
            skymodel=source+'_Q.fits',
            incenter=incenter,
            inwidth=inwidth,
            setpointings=setpointings,
            integration=integration,
            totaltime=totaltime,
            indirection=indirection,
            refdate=refdate,
            hourangle=hourangle,
            obsmode=obsmode,
            antennalist=antennalist,
            thermalnoise=thermalnoise,
            seed=seed,
            graphics=graphics,
            overwrite=overwrite,
            verbose=verbose
        )
        print('\033[1m\n[alma_simulation]\033[0m Observing Stokes U ...\033[0m')
        simobserve(
            project='band6_U',
            skymodel=source+'_U.fits',
            incenter=incenter,
            inwidth=inwidth,
            setpointings=setpointings,
            integration=integration,
            totaltime=totaltime,
            indirection=indirection,
            refdate=refdate,
            hourangle=hourangle,
            obsmode=obsmode,
            antennalist=antennalist,
            thermalnoise=thermalnoise,
            seed=seed,
            graphics=graphics,
            overwrite=overwrite,
            verbose=verbose
        )

if Dirty:
    print('\033[1m\n[alma_simulation] Cleaning Stokes I ...\033[0m')
    tclean(
        vis='band6_I/band6_I.'+vis,
        imagename='band6_I/dirty_I',
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
            imagename='band6_Q/dirty_Q',
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
            imagename='band6_U/dirty_U',
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

    imregrid('band6_I/dirty_I.image', template='band6_I/band6_I.'+antenna+'.skymodel.flat',
             output='band6_I/dirty_I.image_modelsize', overwrite=True)
    exportfits('band6_I/dirty_I.image_modelsize',
               fitsimage='synobs_1300_I.fits', dropdeg=True, overwrite=True)
    exportfits('band6_I/dirty_I.image',
               fitsimage='band6_I/dirty_I.fits', dropdeg=True, overwrite=True)

    if polarization:
        imregrid('band6_Q/dirty_Q.image', template='band6_Q/band6_Q.'+antenna+'.skymodel.flat',
                 output='band6_Q/dirty_Q.image_modelsize', overwrite=True)
        imregrid('band6_U/dirty_U.image', template='band6_U/band6_U.'+antenna+'.skymodel.flat',
                 output='band6_U/dirty_U.image_modelsize', overwrite=True)
        exportfits('band6_Q/dirty_Q.image_modelsize',
                   fitsimage='synobs_1300_Q.fits', dropdeg=True, overwrite=True)
        exportfits('band6_Q/dirty_Q.image',
                   fitsimage='band6_Q/dirty_Q.fits', dropdeg=True, overwrite=True)
        exportfits('band6_U/dirty_U.image_modelsize',
                   fitsimage='synobs_1300_U.fits', dropdeg=True, overwrite=True)
        exportfits('band6_U/dirty_U.image',
                   fitsimage='band6_U/dirty_U.fits', dropdeg=True, overwrite=True)

print('\n[alma_simulaton] Elapsed time: {}'
      .format(time.strftime("%H:%M:%S", time.gmtime(time.time()-start)))
      )

# getting rms information and writing in to a data file
Istat = imstat('band6_I/dirty_I.fits', box='1076,346,1392,589')
Qstat = imstat('band6_Q/dirty_Q.fits', box='1076,346,1392,589')

with open('rms_alma.txt', 'w') as file:
    # Write some text to the file
    file.write(str(Istat['rms'].item()) + '\n')
    file.write(str(Qstat['rms'].item()) + '\n')