"""
Compare Autocorrelation function (ACF) profiles across brain regions.

The script reads data contained in the csv file specified by data_name,
where the ACF values for each channel are already stored.
The test_name file allows to run Linear Mixed models tests of significance.

The data is then plotted in as the mean for each region at every time-lag.
"""

from os import path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils.R_convert import run_R_test_regs_multiple
from utils import plot_seq_regs
from utils.helpers import compute_sig_blocks
from utils.plot_helpers import save_fig, fsize, set_font_params, reset_default_rc

###
# Paths and parameters
###

base_path = ""
data_dir = ""
data_name = ""
test_dir = "LMEs"
test_name = "LME_regs_multiple.R"
save_dir = "Autocorrelation"
save_name = "ACF_regs"
save_format = "svg"

# Set font parameters for plots
set_font_params()

###
# Load data
###

df_acf = pd.read_csv(path.join(base_path, data_dir, data_name), index_col=0)

###
# Complete dataset
###

# Run LME test
source_path = "./" + test_dir + "/" + test_name
save_path = base_path + save_dir + "/"
df_coef, df_stats = run_R_test_regs_multiple(
    source_path, df_acf, save_path, save_name_add="ACF"
)

# Format dataframes
cols_mean = [c for c in df_coef.columns if "mean" in c]
df_mean = df_coef.loc[:, cols_mean].copy()
df_mean.columns = [c.split("_")[0] for c in df_mean.columns]
cols_sem = [c for c in df_coef.columns if "sem" in c]
df_sem = df_coef.loc[:, cols_sem].copy()
df_sem.columns = [c.split("_")[0] for c in df_sem.columns]

# Plot: ACF profiles per region
lags = df_acf.columns[3:].astype(np.float64)
lags_sign_blocks = compute_sig_blocks(df_stats.pval, alpha=0.05)
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax = plot_seq_regs.plot(
    ax,
    lags,
    df_mean,
    df_sem,
    sign_blocks=lags_sign_blocks,
    xticks=np.arange(0, 260, 50),
    yticks=[0, 0.2, 1 / np.e, 0.6, 0.8, 1.0],
    xlabel="Time-lag [ms]",
    ylabel="Autocorrelation",
    linewidth=2,
)
ax.set_yticklabels([0, 0.2, "1/e", 0.6, 0.8, 1.0], fontsize=fsize.TICK_SIZE)
ax.axhline(1 / np.e, lw=0.5, ls="--", c="k")
save_fig(fig, path.join(base_path, save_dir), save_name, save_format)


###
# Restricted on responsive
###

# Run LME test
df_acf_resp = df_acf[df_acf.resp == 1]
df_coef, df_stats = run_R_test_regs_multiple(
    source_path, df_acf_resp, save_path, save_name_add="ACF_resp"
)

# Format dataframes
cols_mean = [c for c in df_coef.columns if "mean" in c]
df_mean = df_coef.loc[:, cols_mean].copy()
df_mean.columns = [c.split("_")[0] for c in df_mean.columns]
cols_sem = [c for c in df_coef.columns if "sem" in c]
df_sem = df_coef.loc[:, cols_sem].copy()
df_sem.columns = [c.split("_")[0] for c in df_sem.columns]

# Plot: ACF profiles per region
lags = df_acf_resp.columns[3:].astype(np.float64)
lags_sign_blocks = compute_sig_blocks(df_stats.pval, alpha=0.05)
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax = plot_seq_regs.plot(
    ax,
    lags,
    df_mean,
    df_sem,
    sign_blocks=lags_sign_blocks,
    xticks=np.arange(0, 260, 50),
    yticks=[0, 0.2, 1 / np.e, 0.6, 0.8, 1.0],
    xlabel="Time-lag [ms]",
    ylabel="Autocorrelation",
    linewidth=2,
)
ax.set_yticklabels([0, 0.2, "1/e", 0.6, 0.8, 1.0], fontsize=fsize.TICK_SIZE)
ax.axhline(1 / np.e, lw=0.5, ls="--", c="k")
save_fig(fig, path.join(base_path, save_dir), save_name + "_resp", save_format)


# Restore params
reset_default_rc()
