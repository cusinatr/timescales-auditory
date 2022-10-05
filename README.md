# Overview
The repo contains the scripts to reproduce the figures in the following paper:

Cusinato, R., Alnes, S. L., van Maren, E., Boccalaro, I., Ledergerber, D., Adamantidis, A., Imbach, L. L., Schindler, K., Baud, M. O., & Tzovara, A. (2022). Intrinsic neural timescales in the temporal lobe support an auditory processing hierarchy. BioRxiv. https://doi.org/10.1101/2022.09.27.509695

Each script usually reproduces just one panel of the figures.
- *LMEs* contains R scripts to run Linear Mixed-Effects models for 'region' effect and regressions.
- *additional* contains scripts to plot timescales, exponent and response parameters across cortical sub-regions-
- *utils* is a collection of scripts mainly containing plotting functions and conversion functions from Python to R.
- *MNI_\*.py* scripts are used for the brain plots, separated by cortex and hippocampus plots.
- *\*_compare_regs.py* scripts are used for plotting raincloud category plots.
- *\*_vs_resp.py* scripts are used for the regression analyses and plots.

## Dependencies
- python == 3.9.12
- numpy == 1.22.3
- scipy == 1.7.3
- pandas == 1.4.3
- matplotlib == 3.5.1
- nilearn == 0.9.1
- rpy2 == 3.5.3
