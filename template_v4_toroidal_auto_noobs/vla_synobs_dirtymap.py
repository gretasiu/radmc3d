# Setup based on Liu et al. (2018)
# Antenna configuration provided in CASA: https://casaguides.nrao.edu/index.php?title=Antenna_Configurations_Models_in_CASA_Cycle5
# To execute them, just keep the script in the folder containing the fitsfiles and run $ casa -c vla_polarization_simulation.py

import time
import random

Simobserve = True
Dirty = True
polarization = True

start = time.time()

# parameters for both synthetic observation and cleaning
antenna = 'vla.d'

# parameters for synthetic observation
source = 'radmc3d_7000'
incenter = '44GHz'
inwidth = '8GHz'
setpointings = True
integration = '2s'
totaltime = '2.5h'
indirection = 'J2000 18h47m34.308 -01d12m45.90'
refdate = '2021/03/31'
hourangle = 'transit'
obsmode = 'int'
antennalist = antenna+'.cfg'
thermalnoise = 'tsys-atm'
graphics = 'file'
overwrite = True
verbose = True

# paramters for cleaning
vis = antenna+'.noisy.ms'
imsize = 323        # No. of cell on in each axis
cell = '0.3arcsec'
reffreq = '44GHz'
specmode = 'mfs'
gridder = 'standard'
deconvolver = 'hogbom'
weighting = 'briggs'
robust = 2                 # turn this on if weighting = 'briggs'
niter = 0
# uvtaper='0.1arcsec'
# mask='centerbox[[200pix, 200pix], [50pix, 50pix]]'
threshold_I = '2.0e-5Jy'
threshold_QU = '2.0e-6Jy'
pbcor = True
interactive = False
verbose = True

if Simobserve:
    print('\033[1m\n[vla_simulation] Observing Stokes I ...\033[0m')
    simobserve(
        project='bandQ_I',
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
        graphics=graphics,
        overwrite=overwrite,
        verbose=verbose
    )
    if polarization:
        print('\033[1m\n[vla_simulation] Observing Stokes Q ...\033[0m')
        simobserve(
            project='bandQ_Q',
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
            graphics=graphics,
            overwrite=overwrite,
            verbose=verbose
        )
        print('\033[1m\n[vla_simulation]\033[0m Observing Stokes U ...\033[0m')
        simobserve(
            project='bandQ_U',
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
            graphics=graphics,
            overwrite=overwrite,
            verbose=verbose
        )

if Dirty:
    print('\033[1m\n[vla_simulation] Cleaning Stokes I ...\033[0m')
    tclean(
        vis='bandQ_I/bandQ_I.'+vis,
        imagename='bandQ_I/dirty_I',
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
            imagename='bandQ_Q/dirty_Q',
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
            imagename='bandQ_U/dirty_U',
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

    imregrid('bandQ_I/dirty_I.image', template='bandQ_I/bandQ_I.'+antenna+'.skymodel.flat',
             output='bandQ_I/dirty_I.image_modelsize', overwrite=True)
    exportfits('bandQ_I/dirty_I.image_modelsize',
               fitsimage='synobs_7000_I.fits', dropdeg=True, overwrite=True)
    exportfits('bandQ_I/dirty_I.image',
               fitsimage='bandQ_I/dirty_I.fits', dropdeg=True, overwrite=True)

    if polarization:
        imregrid('bandQ_Q/dirty_Q.image', template='bandQ_Q/bandQ_Q.'+antenna+'.skymodel.flat',
                 output='bandQ_Q/dirty_Q.image_modelsize', overwrite=True)
        imregrid('bandQ_U/dirty_U.image', template='bandQ_U/bandQ_U.'+antenna+'.skymodel.flat',
                 output='bandQ_U/dirty_U.image_modelsize', overwrite=True)
        exportfits('bandQ_Q/dirty_Q.image_modelsize',
                   fitsimage='synobs_7000_Q.fits', dropdeg=True, overwrite=True)
        exportfits('bandQ_Q/dirty_Q.image',
                   fitsimage='bandQ_Q/dirty_Q.fits', dropdeg=True, overwrite=True)
        exportfits('bandQ_U/dirty_U.image_modelsize',
                   fitsimage='synobs_7000_U.fits', dropdeg=True, overwrite=True)
        exportfits('bandQ_U/dirty_U.image',
                   fitsimage='bandQ_U/dirty_U.fits', dropdeg=True, overwrite=True)

print('\n[vla_simulation] Elapsed time: {}'
      .format(time.strftime("%H:%M:%S", time.gmtime(time.time()-start)))
      )

# getting rms information and writing in to a data file
Istat = imstat('bandQ_I/dirty_I.fits', box='179,64,256,116')
Qstat = imstat('bandQ_Q/dirty_Q.fits', box='179,64,256,116')

with open('rms_vla.txt', 'w') as file:
    # Write some text to the file
    file.write(str(Istat['rms'].item()) + '\n')
    file.write(str(Qstat['rms'].item()) + '\n')