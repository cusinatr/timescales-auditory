"""
Plot response onset and peak latencies across cortex sub-regions.

The script reads data contained in the csv file specified by data_name,
where the timescale for each channel are already stored.
The test_name file allows to run Linear Mixed models tests of significance.

The data is then plotted in sctater plots showing values for each sub-region.
"""
import sys

sys.path.append(".")
from os import path
import pandas as pd
import matplotlib.pyplot as plt

from utils import plot_cat_subregs
from utils.plot_helpers import save_fig, set_font_params, reset_default_rc


###
# Paths and parameters
###

base_path = ""
data_dir = ""
data_name = ""
test_dir = "LMEs"
test_name = "LME_subregs_single.R"
save_dir = "Responses"
save_format = "svg"

# Set font parameters for plots
set_font_params()

###
# Load data
###

df_resp = pd.read_csv(path.join(base_path, data_dir, data_name), index_col=0)
df_resp = df_resp[df_resp.region == "CTX"]
df_resp.drop(columns="region", inplace=True)
df_resp.rename(columns={"subreg": "region"}, inplace=True)
df_resp.dropna(inplace=True)

###
# Replace codes with "grouped" subregions
###

df_resp.region = df_resp.region.replace(
    {
        "TTG": "Transverse",
        "STG": "Superior",
        "STS": "Superior",
        "MTG": "Middle",
        "ITG": "Inferior",
        "ITS": "Inferior",
        "INSULA": "Insula",
        "POLE": "Pole",
    }
)

###
# Onsets
###

# Plot: distribution of characteristic timescales per region
df_plot = df_resp.copy()
fig, ax = plt.subplots(1, 1, figsize=(8, 5))
ax = plot_cat_subregs.plot(
    ax,
    df_plot,
    "onset",
    means_prec=1,
    ylabel=r"Auditory iERP Onset [ms]",
    yticks=100,
    yscale=(0, None),
)

save_fig(fig, path.join(base_path, save_dir), "Onset_subregs", save_format)


###
# Peaks
###

# Plot: distribution of characteristic timescales per region
df_plot = df_resp.copy()
fig, ax = plt.subplots(1, 1, figsize=(8, 5))
ax = plot_cat_subregs.plot(
    ax,
    df_plot,
    "peak",
    means_prec=1,
    ylabel=r"Auditory iERP Peak [ms]",
    yticks=100,
    yscale=(0, None),
)
save_fig(fig, path.join(base_path, save_dir), "Peak_subregs", save_format)

# Restore params
reset_default_rc()

