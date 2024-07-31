# radmc3d

"template_v4_toroidal_auto" is the template directory each trial run is based on. It contains setup script for running radmc3d, synethetic observation, cleaning and visualizaion using aplpy. It also contains a shell script "exe.sh" that carry out these steps. <br>

control.sh controls the whole process of a trial. The aim of this script is to streamline parameter search process for a given B field model. Parameters can be specified within control.sh. It can handle a combination of parameters. The script duplicates the "template_v4_toroidal_auto" directory for each parameter combination and call "exe.sh" within each new directory. <br>

Two environments are needed in running this control.sh.<br>
- base environment in which control.sh is run. <br>
- an environment to run visualization using aplpy called "aplpy_env". <br>

Please see the requirement text file for these two environments.<br>
Run control.sh in the base environment. "aplpy_env" will be automatically activated during the visualization step.<br>
