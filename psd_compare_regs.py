"""
Compare Power Spectral Density (PSD) profiles across brain regions.

The script reads data contained in the csv file specified by data_name,
where the PSD values for each channel are already stored.
The test_name file allows to run Linear Mixed models tests of significance.

The data is then plotted in as the mean for each region at every frequency.
"""

from os import path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils.R_convert import run_R_test_regs_multiple
from utils import plot_seq_regs
from utils.plot_helpers import save_fig, color, fsize, set_font_params, reset_default_rc

###
# Paths and parameters
###

base_path = ""
data_dir = ""
data_name = ""
test_dir = "LMEs"
test_name = "LME_regs_multiple.R"
save_dir = "PSD"
save_name = "PSD_regs"
save_format = "svg"

freqs_plot = [1, 150]

# Set font parameters for plots
set_font_params()

###
# Load data
###

df_psd = pd.read_csv(path.join(base_path, data_dir, data_name), index_col=0)
freqs = df_psd.columns[3:].astype(np.float64)
freqs = freqs[np.logical_and(freqs >= freqs_plot[0], freqs <= freqs_plot[1])]
df_psd = df_psd.loc[:, ["chan", "resp", "region"] + [str(f) for f in freqs]]

# Transform in log
df_psd.iloc[:, 3:] = np.log10(df_psd.iloc[:, 3:])

###
# Complete dataset
###

# Run LME test
source_path = "./" + test_dir + "/" + test_name
save_path = base_path + save_dir + "/"
df_coef, _ = run_R_test_regs_multiple(
    source_path, df_psd, save_path, save_name_add="PSD"
)

# Format dataframes
cols_mean = [c for c in df_coef.columns if "mean" in c]
df_mean = df_coef.loc[:, cols_mean].copy()
df_mean.columns = [c.split("_")[0] for c in df_mean.columns]
cols_sem = [c for c in df_coef.columns if "sem" in c]
df_sem = df_coef.loc[:, cols_sem].copy()
df_sem.columns = [c.split("_")[0] for c in df_sem.columns]

# Plot: ACF profiles per region
fig, ax = plt.subplots(1, 1, figsize=(3.5, 7))
ax = plot_seq_regs.plot(
    ax,
    freqs,
    df_mean,
    df_sem,
    add_sign=False,
    logx=True,
    logy=False,
    xticks=[1, 10, 100, 150],
    yticks=[np.log10(0.002), np.log10(250)],
    xlabel="Frequency [Hz]",
    ylabel=r"PSD [$\mu V^2$/Hz]",
    linewidth=2,
)
# Aperiodic fit limits
ax.axvspan(20, 35, color=color.brown, alpha=0.2)
ax.axvspan(80, 150, color=color.brown, alpha=0.2)
# Set axes limits and ticks
ax.set_xlim(freqs_plot)
ax.set_ylim(-2.8, 2.4)
ax.set_yticklabels([0.002, 250], fontsize=fsize.TICK_SIZE)

save_fig(fig, path.join(base_path, save_dir), save_name, save_format)


###
# Restricted on responsive
###

# Run LME test
df_psd_resp = df_psd[df_psd.resp == 1]
df_coef, _ = run_R_test_regs_multiple(
    source_path, df_psd_resp, save_path, save_name_add="PSD_resp"
)

# Format dataframes
cols_mean = [c for c in df_coef.columns if "mean" in c]
df_mean = df_coef.loc[:, cols_mean].copy()
df_mean.columns = [c.split("_")[0] for c in df_mean.columns]
cols_sem = [c for c in df_coef.columns if "sem" in c]
df_sem = df_coef.loc[:, cols_sem].copy()
df_sem.columns = [c.split("_")[0] for c in df_sem.columns]

# Plot: ACF profiles per region
fig, ax = plt.subplots(1, 1, figsize=(3.5, 7))
ax = plot_seq_regs.plot(
    ax,
    freqs,
    df_mean,
    df_sem,
    add_sign=False,
    logx=True,
    logy=False,
    xticks=[1, 10, 100, 150],
    yticks=[np.log10(0.002), np.log10(250)],
    xlabel="Frequency [Hz]",
    ylabel=r"PSD [$\mu V^2$/Hz]",
    linewidth=2,
)
# Aperiodic fit limits
ax.axvspan(20, 35, color=color.brown, alpha=0.2)
ax.axvspan(80, 150, color=color.brown, alpha=0.2)
# Set axes limits and ticks
ax.set_xlim(freqs_plot)
ax.set_ylim(-2.8, 2.4)
ax.set_yticklabels([0.002, 250], fontsize=fsize.TICK_SIZE)

save_fig(fig, path.join(base_path, save_dir), save_name + "_resp", save_format)

# Restore params
reset_default_rc()
