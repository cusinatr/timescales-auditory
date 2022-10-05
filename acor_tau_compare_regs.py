"""
Plot baseline timescales across brain areas.

The script reads data contained in the csv file specified by data_name,
where the timescale for each channel are already stored.
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
save_dir = "Autocorrelation"
save_name = "Timescale_regs"
save_format = "svg"

# Set font parameters for plots
set_font_params()

###
# Load data
###

df_tau = pd.read_csv(path.join(base_path, data_dir, data_name), index_col=0)
df_tau.drop(columns=["subreg"], inplace=True)

###
# Complete dataset
###

# Run LME test
source_path = "./" + test_dir + "/" + test_name
save_path = base_path + save_dir + "/"
df_coef, df_stats = run_R_test_regs(source_path, df_tau, "tau", save_path)

# Plot: distribution of characteristic timescales per region
df_plot = df_tau.copy()
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax = plot_cat_regs.plot(
    ax,
    df_plot,
    "tau",
    means=df_coef.Coef.to_numpy(),
    SEMs=df_coef.SE.to_numpy(),
    means_prec=1,
    ylabel=r"Baseline $\tau$ [ms]",
    yticks=20,
    yscale=(0, None),
)
# ax.set_yscale("log")
# Add significance bars
ax = catplot_annot_sign(ax, df_stats, dh=0.02, write_ns=False,)
save_fig(fig, path.join(base_path, save_dir), save_name, save_format)


###
# Restricted on responsive
###

# Run LME test
df_tau_resp = df_tau[df_tau.resp == 1]
df_coef_resp, df_stats_resp = run_R_test_regs(
    source_path, df_tau_resp, "tau", save_path, save_name_add="resp"
)

# Plot: distribution of characteristic timescales per region
df_plot = df_tau_resp.copy()
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax = plot_cat_regs.plot(
    ax,
    df_plot,
    "tau",
    means=df_coef_resp.Coef.to_numpy(),
    SEMs=df_coef_resp.SE.to_numpy(),
    means_prec=1,
    ylabel=r"Baseline $\tau$ [ms]",
    yticks=20,
    yscale=(0, None),
)
ax = catplot_annot_sign(ax, df_stats_resp, dh=0.02, write_ns=False,)
save_fig(fig, path.join(base_path, save_dir), save_name + "_resp", save_format)

# Restore params
reset_default_rc()
