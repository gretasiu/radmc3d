'''
Analysis of the results from snyons to find the best fit model 

This code produces:
1. intensity comparison of synethtic observation and real observation of 1.3mm and 7mm on the same plot
2. side-by-side comparisons of PI and Pf
3. PA differences histogram and statistic
'''
import matplotlib.pyplot as plt
import numpy as np
from aplpy import FITSFigure
from astropy import wcs
from astropy.coordinates import SkyCoord
import g31_utils as g31u

intensity_comparision = True
pi_pf_comparison_13 = True
pi_pf_comparison_70 = True

# Getting intensity data from FITS files
syn_intensity_13 = g31u.FITSimage('synobs_1300_I.fits')
syn_intensity_13.FITSdata()
# syn_pi_13 = g31u.FITSimage('synobs_1300_pi.fits')
# syn_pi_13.FITSdata()
syn_intensity_70 = g31u.FITSimage('synobs_7000_I.fits')
syn_intensity_70.FITSdata()

# Getting real obs intensity data from FITS files
real_intensity_13 = g31u.FITSimage('realobs/G31_ALMAb6pol_I.dropdeg.fits')
real_intensity_13.FITSdata()
real_PI_13 = g31u.FITSimage('realobs/G31_ALMAb6pol_PI.miriad.dropdeg.fits')
real_PI_13.FITSdata()
real_Pf_13 = g31u.FITSimage('realobs/G31_ALMAb6pol_Per.miriad.dropdeg.fits')
real_Pf_13.FITSdata()
real_intensity_70 = g31u.FITSimage(
    'realobs/G31p4_Qband_D.rob2.I.image.tt0.dropdeg.fits')
real_intensity_70.FITSdata()
real_PI_70 = g31u.FITSimage(
    'realobs/G31p4_Qband_D.rob2.PI.image.tt0.miriad.dropdeg.fits')
real_PI_70.FITSdata()
real_Pf_70 = g31u.FITSimage(
    'realobs/G31p4_Qband_D.rob2.Per.image.tt0.miriad.dropdeg.fits')
real_Pf_70.FITSdata()

# comparing intensity
if intensity_comparision == True:
    # Extracting 7mm real obs intensity along specified line
    lineStart = [238, 238]
    lineEnd = [223, 229]
    num = 1000
    zoomStart = [210, 210]
    zoomEnd = [269, 269]
    path = 'fig/analysis/70_1D_intensity.pdf'
    distance = 3.75
    pixel_size = 0.3
    line_obs70, intensity_obs70 = g31u.oneDLineExtrater(real_intensity_70.data, lineStart, lineEnd, num, distance, pixel_size,
                                                        zoomStart, zoomEnd, zoom=True, savfig=True, path=path)

    # Extracting 7mm syn obs intensity along specified line
    lineStart = [len(syn_intensity_70.data[0])/2,
                 len(syn_intensity_70.data[1])/2]
    lineEnd = [len(syn_intensity_70.data[0])/2, 0]
    num = 1000
    path = 'fig/analysis/70_synobs_1D_intensity.pdf'
    distance = 3.75
    pixel_size = 0.0107  # 0.0046 for 1.3mm
    line_synobs70, intensity_synobs70 = g31u.oneDLineExtrater(
        syn_intensity_70.data, lineStart, lineEnd, num, distance, pixel_size, zoom=False, savfig=True, path=path)

    # Extracting 1.3mm real obs intensity along specified line
    lineStart = [1019, 1023]
    lineEnd = [1043, 1000]
    num = 1000
    zoomStart = [956, 954]
    zoomEnd = [1081, 1084]
    path = 'fig/analysis/13_1D_intensity.pdf'
    distance = 3.75
    pixel_size = 0.0241
    line_obs13, intensity_obs13 = g31u.oneDLineExtrater(real_intensity_13.data, lineStart, lineEnd, num, distance, pixel_size,
                                                        zoomStart, zoomEnd, zoom=True, savfig=True, path=path)

    # Extracting 1.3mm syn obs intensity along specified line
    lineStart = [len(syn_intensity_13.data[0])/2,
                 len(syn_intensity_13.data[1])/2]
    lineEnd = [len(syn_intensity_13.data[0])/2, 0]
    num = 1000
    path = 'fig/analysis/13_synobs_1D_intensity.pdf'
    distance = 3.75
    pixel_size = 0.0046
    line_synobs13, intensity_synobs13 = g31u.oneDLineExtrater(
        syn_intensity_13.data, lineStart, lineEnd, num, distance, pixel_size, zoom=False, savfig=True, path=path)

    # plotting all intensity comparison on the same plot
    au_to_pc = 4.84814e-6

    def au2pc(au):
        return au*au_to_pc

    def pc2au(au):
        return au/au_to_pc

    # log scale in x- and y-axis only
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    ax.loglog(line_obs70, intensity_obs70,
              color='red', label='7mm JVLA')
    ax.loglog(line_synobs70, intensity_synobs70, linestyle='--', color='red',
              label='7mm synthetic observation')
    ax.loglog(line_obs13, intensity_obs13,
              color='blue', label='1.3mm ALMA')
    ax.loglog(line_synobs13, intensity_synobs13, linestyle='--', color='blue',
              label='1.3mm synthetic observation')
    ax.set_xlabel('[AU]', fontsize=16)
    ax.set_ylabel('Jy/beam', fontsize=16)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    secax = ax.secondary_xaxis('top', functions=(au2pc, pc2au))
    secax.set_xlabel('[pc]', fontsize=16)
    secax.tick_params(axis='x', labelsize=16)
    ax.legend()
    plt.savefig('fig/analysis/intensity_comparison_loglog.pdf')
    plt.show()

    # log scale in y-axis only
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    ax.plot(line_obs70, intensity_obs70,
            color='red', label='7mm JVLA')
    ax.plot(line_synobs70, intensity_synobs70, linestyle='--', color='red',
            label='7mm synthetic observation')
    ax.plot(line_obs13, intensity_obs13,
            color='blue', label='1.3mm ALMA')
    ax.plot(line_synobs13, intensity_synobs13, linestyle='--', color='blue',
            label='1.3mm synthetic observation')
    ax.semilogy()
    ax.set_xlabel('[AU]', fontsize=16)
    ax.set_ylabel('Jy/beam', fontsize=16)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    secax = ax.secondary_xaxis('top', functions=(au2pc, pc2au))
    secax.set_xlabel('[pc]', fontsize=16)
    secax.tick_params(axis='x', labelsize=16)
    ax.legend()
    plt.savefig('fig/analysis/intensity_comparison_semilogy.pdf')
    plt.show()

# comparing pi and pf side by side
if pi_pf_comparison_13 == True:
    # Create a figure with multiple subplots
    fig, axarr = plt.subplots(2, 2, figsize=(16, 12))  # 1 row, 2 columns
    # removing boarder created with subplots
    for x in (0, 1):
        for y in (0, 1):
            axarr[x, y].axis('off')

    # Load and customize the first FITS file
    fig1 = FITSFigure(real_PI_13.hdu,
                      figure=fig, subplot=(2, 2, 1))
    fig1.show_colorscale(cmap='viridis')
    fig1.add_colorbar()
    fig1.set_title('1.3mm ALMA PI')
    # recentering realobs
    xpix_temp = int(round(real_PI_13.naxis1/2.0))
    ypix_temp = int(round(real_PI_13.naxis2/2.0))
    world = real_PI_13.hduwcs.wcs_pix2world([[xpix_temp, ypix_temp]], 0)
    ra_center_zoom = world[0][0]
    dec_center_zoom = world[0][1]
    fig1.recenter(ra_center_zoom, dec_center_zoom,
                  width=0.0013, height=0.0013)

    # Load and customize the second FITS file
    fig2 = FITSFigure('synobs_1300_pi.fits', figure=fig, subplot=(2, 2, 2))
    fig2.show_colorscale(cmap='viridis')
    fig2.add_colorbar()
    fig2.set_title('1.3mm synthetic observation PI')

    # Load and customize the third FITS file
    fig1 = FITSFigure(real_Pf_13.hdu,
                      figure=fig, subplot=(2, 2, 3))
    fig1.show_colorscale(cmap='plasma')
    fig1.add_colorbar()
    fig1.set_title('1.3mm ALMA Per')
    # recentering realobs
    xpix_temp = int(round(real_Pf_13.naxis1/2.0))
    ypix_temp = int(round(real_Pf_13.naxis2/2.0))
    world = real_Pf_13.hduwcs.wcs_pix2world([[xpix_temp, ypix_temp]], 0)
    ra_center_zoom = world[0][0]
    dec_center_zoom = world[0][1]
    fig1.recenter(ra_center_zoom, dec_center_zoom,
                  width=0.0013, height=0.0013)

    # Load and customize the forth FITS file
    fig2 = FITSFigure('synobs_1300_pf.fits', figure=fig, subplot=(2, 2, 4))
    fig2.show_colorscale(cmap='plasma')
    fig2.add_colorbar()
    fig2.set_title('1.3mm synthetic observation Per')

    # Customize other properties of each subplot as needed

    # Adjust the spacing between subplots
    # plt.tight_layout()
    plt.savefig('fig/analysis/PI_Per_13')
    plt.show()

if pi_pf_comparison_70 == True:
    # Create a figure with multiple subplots
    fig, axarr = plt.subplots(2, 2, figsize=(16, 12))  # 1 row, 2 columns
    # removing boarder created with subplots
    for x in (0, 1):
        for y in (0, 1):
            axarr[x, y].axis('off')

    # Load and customize the first FITS file
    fig1 = FITSFigure(real_PI_70.hdu,
                      figure=fig, subplot=(2, 2, 1))
    fig1.show_colorscale(cmap='viridis')
    fig1.add_colorbar()
    fig1.set_title('7mm JVLA PI')
    # recentering realobs
    xpix_temp = int(round(real_PI_70.naxis1/2.0))
    ypix_temp = int(round(real_PI_70.naxis2/2.0))
    world = real_PI_70.hduwcs.wcs_pix2world([[xpix_temp, ypix_temp]], 0)
    ra_center_zoom = world[0][0]
    dec_center_zoom = world[0][1]
    fig1.recenter(ra_center_zoom, dec_center_zoom,
                  width=0.003, height=0.003)

    # Load and customize the second FITS file
    fig2 = FITSFigure('synobs_7000_pi.fits', figure=fig, subplot=(2, 2, 2))
    fig2.show_colorscale(cmap='viridis')
    fig2.add_colorbar()
    fig2.set_title('7mm synthetic observation PI')

    # Load and customize the third FITS file
    fig1 = FITSFigure(real_Pf_70.hdu,
                      figure=fig, subplot=(2, 2, 3))
    fig1.show_colorscale(cmap='plasma')
    fig1.add_colorbar()
    fig1.set_title('7mm JVLA Per')
    # recentering realobs
    xpix_temp = int(round(real_PI_70.naxis1/2.0))
    ypix_temp = int(round(real_PI_70.naxis2/2.0))
    world = real_PI_70.hduwcs.wcs_pix2world([[xpix_temp, ypix_temp]], 0)
    ra_center_zoom = world[0][0]
    dec_center_zoom = world[0][1]
    fig1.recenter(ra_center_zoom, dec_center_zoom,
                  width=0.003, height=0.003)

    # Load and customize the forth FITS file
    fig2 = FITSFigure('synobs_7000_pf.fits', figure=fig, subplot=(2, 2, 4))
    fig2.show_colorscale(cmap='plasma')
    fig2.add_colorbar()
    fig2.set_title('7mm synthetic observation Per')

    # Customize other properties of each subplot as needed

    # Adjust the spacing between subplots
    # plt.tight_layout()
    plt.savefig('fig/analysis/PI_Per_70')
    plt.show()
