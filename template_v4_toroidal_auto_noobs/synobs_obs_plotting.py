import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
#parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

import g31_utils as u
import utils as utils
import numpy as np

##########################################################################################################
# Button
##########################################################################################################
synobs_1300 = True
synobs_on_obs_1300 = True
synobs_7000 = True
synobs_on_obs_7000 = True

##########################################################################################################
# Creating APLpy readable IQU, PA, PI and Per fits files
##########################################################################################################
fig = utils.polarization_map(
    source='synobs_1300', render='I', step=30, const_pfrac=True, scale=10)
fig = utils.polarization_map(
    source='synobs_7000', render='I', step=30, const_pfrac=True, scale=10)

##########################################################################################################
# Importing fits file
##########################################################################################################
# synobs
alma_I_synobs = u.FITSimage('synobs_1300_I.fits')
alma_I_synobs.FITSdata()
alma_pa_synobs = u.FITSimage('synobs_1300_pa.fits')
alma_pa_synobs.FITSdata()
jvla_I_synobs = u.FITSimage('synobs_7000_I.fits')
jvla_I_synobs.FITSdata()
jvla_pa_synobs = u.FITSimage('synobs_7000_pa.fits')
jvla_pa_synobs.FITSdata()
# real obs
alma_I = u.FITSimage('realobs/G31_ALMAb6pol_I.dropdeg.fits')
alma_I.FITSdata()
alma_pa = u.FITSimage('realobs/G31_ALMAb6pol_PA.miriad.dropdeg.fits')
alma_pa.FITSdata()
jvla_I = u.FITSimage('realobs/G31p4_Qband_D.rob2.I.image.tt0.dropdeg.fits')
jvla_I.FITSdata()
jvla_pa = u.FITSimage('realobs/G31p4_Qband_D.rob2.PA.image.tt0.miriad.dropdeg.fits')
jvla_pa.FITSdata()

##########################################################################################################
# Selecting data to plot
##########################################################################################################
alma_pa_synobs.data[np.isnan(alma_pa.data)] = np.nan
jvla_pa_synobs.data[np.isnan(jvla_pa.data)] = np.nan

##########################################################################################################
# Plotting 1300 synobs PA on I
##########################################################################################################
if synobs_1300:
    outfigname = 'fig/synobs_1300_PA_on_I_test.pdf'
    Ihdu = alma_I_synobs
    PAhdu = [alma_pa_synobs]
    beamhdu = [alma_I_synobs]
    #contourlevel = [[10, 20, 30, 40]]
    plot_Bvector = [True]
    length_control = [0.4]
    linewidth = [2.5]
    vector_space = [20]
    jvla_ra, jvla_dec = alma_I_synobs.FITScenter(0, 0)
    width = 16
    height = 16
    colorbar_label = 'I (Jy/beam)'
    tick_font = 12
    u.aplyPy_plot(outfigname=outfigname, Ihdu=Ihdu, PAhdu=PAhdu, beamhdu=beamhdu,
                plot_Bvector=plot_Bvector, ra_center=jvla_ra, dec_center=jvla_dec,
                width=width, height=height, colorbar_label=colorbar_label, 
                length_control=length_control, linewidth=linewidth, vector_space=vector_space, 
                tick_font=tick_font)
    

##########################################################################################################
# Plotting synobs PA on real obs I and PA
##########################################################################################################
if synobs_on_obs_1300:
    outfigname = 'fig/synobs_1300_PA_on_almaIPA_regrid_B_test.pdf'
    Ihdu = alma_I
    PAhdu = [alma_pa, alma_pa_synobs]
    beamhdu = [alma_I]
    #contourlevel = [[10, 20, 30, 40]]
    plot_Bvector = [True, False]
    length_control = [0.4, 0.4]
    linewidth = [2.5, 2.5]
    vector_space = [20, 20]
    jvla_ra, jvla_dec = alma_I_synobs.FITScenter(0, 0)
    width = 16
    height = 16
    colorbar_label = 'I (Jy/beam)'
    tick_font = 12
    u.aplyPy_plot(outfigname=outfigname, Ihdu=Ihdu, PAhdu=PAhdu, beamhdu=beamhdu,
                plot_Bvector=plot_Bvector, ra_center=jvla_ra, dec_center=jvla_dec,
                width=width, height=height, colorbar_label=colorbar_label, 
                length_control=length_control, linewidth=linewidth, vector_space=vector_space, 
                tick_font=tick_font)
    
##########################################################################################################
# Calculating PA difference for only the vectors plotted
##########################################################################################################
u.pa_difference(alma_pa, alma_pa_synobs, vector_space[0], 10, 'fig/alma_pa_difference.pdf')

##########################################################################################################
# Plotting 1300 synobs PA on I
##########################################################################################################
if synobs_7000:
    outfigname = 'fig/synobs_7000_PA_on_I_test.pdf'
    Ihdu = jvla_I_synobs
    PAhdu = [jvla_pa_synobs]
    beamhdu = [jvla_I_synobs]
    #contourlevel = [[10, 20, 30, 40]]
    plot_Bvector = [True]
    length_control = [3.5]
    linewidth = [3]
    vector_space = [2]
    jvla_ra, jvla_dec = jvla_I_synobs.FITScenter(0, 0)
    width = 16
    height = 16
    colorbar_label = 'I (Jy/beam)'
    tick_font = 12
    u.aplyPy_plot(outfigname=outfigname, Ihdu=Ihdu, PAhdu=PAhdu, beamhdu=beamhdu,
                plot_Bvector=plot_Bvector, ra_center=jvla_ra, dec_center=jvla_dec,
                width=width, height=height, colorbar_label=colorbar_label, 
                length_control=length_control, linewidth=linewidth, vector_space=vector_space, 
                tick_font=tick_font)

##########################################################################################################
# Plotting synobs PA on real obs I and PA
##########################################################################################################
if synobs_on_obs_7000:
    outfigname = 'fig/synobs_7000_PA_on_jvlaIPA_regrid_B_test.pdf'
    Ihdu = jvla_I
    PAhdu = [jvla_pa, jvla_pa_synobs]
    beamhdu = [jvla_I]
    #contourlevel = [[10, 20, 30, 40]]
    plot_Bvector = [True, False]
    length_control = [3.5, 3.5]
    linewidth = [3, 3]
    vector_space = [2, 2]
    jvla_ra, jvla_dec = alma_I_synobs.FITScenter(0, 0)
    width = 16
    height = 16
    colorbar_label = 'I (Jy/beam)'
    tick_font = 12
    u.aplyPy_plot(outfigname=outfigname, Ihdu=Ihdu, PAhdu=PAhdu, beamhdu=beamhdu,
                plot_Bvector=plot_Bvector, ra_center=jvla_ra, dec_center=jvla_dec,
                width=width, height=height, colorbar_label=colorbar_label, 
                length_control=length_control, linewidth=linewidth, vector_space=vector_space, 
                tick_font=tick_font)

##########################################################################################################
# Calculating PA difference for only the vectors plotted
##########################################################################################################
u.pa_difference(jvla_pa, jvla_pa_synobs, vector_space[0], 10, 'fig/jvla_pa_difference.pdf')

