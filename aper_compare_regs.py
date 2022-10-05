"""
Plot 1/f exponent and offset across brain areas.

The script reads data contained in the csv file specified by data_name,
where the 1/f parameters for each channel are already stored.
The test_name file allows to run Linear Mixed models tests of significance.

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
save_dir = "Aperiodic"
save_name = "Aper_regs"
save_test_name = ""
save_format = "svg"

# Set font parameters for plots
set_font_params()

###
# Load data
###

df_aper = pd.read_csv(path.join(base_path, data_dir, data_name), index_col=0)
df_aper.drop(columns=["subreg"], inplace=True)

###
# Complete dataset
###

# EXPONENT

# Run LME test
source_path = "./" + test_dir + "/" + test_name
save_path = base_path + save_dir + "/"
df_coef, df_stats = run_R_test_regs(
    source_path, df_aper, "exp", save_path, save_name_add=save_test_name
)

# Plot: distribution of characteristic timescales per region
df_plot = df_aper.copy()
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax = plot_cat_regs.plot(
    ax,
    df_plot,
    "exp",
    means=df_coef.Coef.to_numpy(),
    SEMs=df_coef.SE.to_numpy(),
    means_prec=1,
    ylabel="Baseline exponent [a.u.]",
    yticks=2,
    yscale=(0, None),
)
# Add significance bars
ax = catplot_annot_sign(ax, df_stats, dh=0.02, write_ns=False,)
save_fig(fig, path.join(base_path, save_dir), save_name + "_exp", save_format)

# OFFSET

# Run LME test
source_path = "./" + test_dir + "/" + test_name
save_path = base_path + save_dir + "/"
df_coef, df_stats = run_R_test_regs(
    source_path, df_aper, "off", save_path, save_name_add=save_test_name
)

# Plot: distribution of characteristic timescales per region
df_plot = df_aper.copy()
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax = plot_cat_regs.plot(
    ax,
    df_plot,
    "off",
    means=df_coef.Coef.to_numpy(),
    SEMs=df_coef.SE.to_numpy(),
    means_prec=1,
    ylabel="Baseline offset [a.u.]",
    yticks=2,
    yscale=(0, None),
)
# Add significance bars
ax = catplot_annot_sign(ax, df_stats, dh=0.02, write_ns=False,)
save_fig(fig, path.join(base_path, save_dir), save_name + "_off", save_format)


###
# Restricted on responsive
###

# EXPONENT

# Run LME test
df_aper_resp = df_aper[df_aper.resp == 1]
df_coef_resp, df_stats_resp = run_R_test_regs(
    source_path, df_aper_resp, "exp", save_path, save_name_add="resp_" + save_test_name
)

# Plot: distribution of characteristic timescales per region
df_plot = df_aper_resp.copy()
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax = plot_cat_regs.plot(
    ax,
    df_plot,
    "exp",
    means=df_coef_resp.Coef.to_numpy(),
    SEMs=df_coef_resp.SE.to_numpy(),
    means_prec=1,
    ylabel="Baseline exponent [a.u.]",
    yticks=2,
    yscale=(0, None),
)
ax = catplot_annot_sign(ax, df_stats_resp, dh=0.02, write_ns=False,)
save_fig(fig, path.join(base_path, save_dir), save_name + "_exp_resp", save_format)

# OFFSET

# Run LME test
df_coef_resp, df_stats_resp = run_R_test_regs(
    source_path, df_aper_resp, "off", save_path, save_name_add="resp_" + save_test_name
)

# Plot: distribution of characteristic timescales per region
df_plot = df_aper_resp.copy()
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax = plot_cat_regs.plot(
    ax,
    df_plot,
    "off",
    means=df_coef_resp.Coef.to_numpy(),
    SEMs=df_coef_resp.SE.to_numpy(),
    means_prec=1,
    ylabel="Baseline offset [a.u.]",
    yticks=2,
    yscale=(0, None),
)
ax = catplot_annot_sign(ax, df_stats_resp, dh=0.02, write_ns=False,)
save_fig(fig, path.join(base_path, save_dir), save_name + "_off_resp", save_format)

# Restore params
reset_default_rc()
