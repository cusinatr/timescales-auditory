"""
Plot responses onset and peak latencies across brain areas.

The script reads data contained in the csv file specified by data_name,
where the parameters for each responsive channel are already stored.
The test_name file allows to run Mixed models tests of significance.

The data is then plotted in raincluoud plots (scatter and violin plots)
showing values for each region.
"""

from os import path
import pandas as pd
import matplotlib.pyplot as plt

from utils.R_convert import run_R_test_regs
from utils import plot_cat_regs
from utils.plot_significance import catplot_annot_sign
from utils.plot_helpers import save_fig, set_font_params, reset_default_rc

###
# Paths and parameters
###

base_path = ""
data_dir = ""
data_name = ""
test_dir = "LMEs"
test_name = "LME_regs_single.R"
save_dir = "Responses"
save_format = "svg"

# Set font parameters for plots
set_font_params()

###
# Load data
###

df_resp = pd.read_csv(path.join(base_path, data_dir, data_name), index_col=0)
df_resp.drop(columns=["subreg"], inplace=True)

###
# Run LME tests
###

source_path = "./" + test_dir + "/" + test_name
save_path = base_path + save_dir + "/"
df_coef_onset, df_stats_onset = run_R_test_regs(
    source_path, df_resp, "onset", save_path
)
df_coef_peak, df_stats_peak = run_R_test_regs(source_path, df_resp, "peak", save_path)

###
# Plot distributions per region
###

# Onsets
df_plot = df_resp.copy()
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax = plot_cat_regs.plot(
    ax,
    df_plot,
    "onset",
    means=df_coef_onset.Coef.to_numpy(),
    SEMs=df_coef_onset.SE.to_numpy(),
    means_prec=1,
    ylabel=r"Auditory iERP Onset [ms]",
    yticks=100,
    yscale=(0, 650),
)
ax.set_ylim(0, 650)
# Add significance bars
ax = catplot_annot_sign(ax, df_stats_onset, dh=0.02, write_ns=False,)
save_fig(fig, path.join(base_path, save_dir), "Onset_regs", save_format)

# Peaks
df_plot = df_resp.copy()
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax = plot_cat_regs.plot(
    ax,
    df_plot,
    "peak",
    means=df_coef_peak.Coef.to_numpy(),
    SEMs=df_coef_peak.SE.to_numpy(),
    means_prec=1,
    ylabel=r"Auditory iERP Peak [ms]",
    yticks=100,
    yscale=(0, 650),
)
ax.set_ylim(0, 650)
# Add significance bars
ax = catplot_annot_sign(ax, df_stats_peak, dh=0.02, write_ns=False,)
save_fig(fig, path.join(base_path, save_dir), "Peak_regs", save_format)

# Restore params
reset_default_rc()
