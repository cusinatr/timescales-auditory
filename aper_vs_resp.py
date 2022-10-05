"""
Plot correlation of 1/f exponent with auditory evoked responses latencies.

The script reads data contained in the csv file specified by data_name and resp_name,
where the exponent and latencies for each channel are already stored.
The test_name file allows to run Linear Mixed models tests of significance.

The data is then plotted in scatter plots both 'globally' and restriced on
each region.
"""

from os import path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils.helpers import get_resp_params
from utils.R_convert import run_R_test_corr
from utils import plot_corr
from utils.plot_helpers import save_fig, color, set_font_params, reset_default_rc


###
# Paths and parameters
###

base_path = ""
data_dir = ""
data_name = ""
resp_name = ""
test_dir = "LMEs"
test_name = "LME_corr.R"
save_dir = "Responses"
save_name = "Corr_exp"
save_format = "svg"

# Set font parameters for plots
set_font_params()

###
# Load timescales and responses parameters files
###

df_aper = pd.read_csv(path.join(base_path, data_dir, data_name), index_col=0)
df_resp = pd.read_csv(path.join(base_path, data_dir, resp_name), index_col=0)

###
# Compute single dataframe with all parameters
###

df_data = get_resp_params(df_resp, df_aper, ["exp"])

###
# Run LME test
###

source_path = "./" + test_dir + "/" + test_name
save_path = base_path + save_dir + "/"
df_test_onset = run_R_test_corr(source_path, df_data, "exp", "onset", save_path)
df_test_peak = run_R_test_corr(source_path, df_data, "exp", "peak", save_path)

# Re-index with 'Group' column
df_test_onset = df_test_onset.set_index("Group")
df_test_peak = df_test_peak.set_index("Group")

###
# 1) Correlation with all regions together
###

# Onset
fig, ax = plt.subplots(1, 1, figsize=[5, 5])
ax = plot_corr.plot(
    ax,
    df_data["exp"],
    df_data.onset,
    df_fit=df_test_onset.loc["Overall"],
    xy_annot=(0.75, 0.05),
    ylabel="Auditory iERP Onset [ms]",
    xlabel="Baseline exponent [a.u.]",
    xticks=np.arange(1, 7, 1),
    yticks=np.arange(0, 601, 100),
)
ax.set_ylim(0, 650)
save_fig(
    fig, path.join(base_path, save_dir), "Corr_onset_exp_all", format=save_format,
)

# Peak
fig, ax = plt.subplots(1, 1, figsize=[5, 5])
ax = plot_corr.plot(
    ax,
    df_data["exp"],
    df_data.peak,
    df_fit=df_test_peak.loc["Overall"],
    xy_annot=(0.7, 0.05),
    ylabel="Auditory iERP Peak [ms]",
    xlabel="Baseline exponent [a.u.]",
    xticks=np.arange(1, 7, 1),
    yticks=np.arange(0, 601, 100),
)
ax.set_ylim(0, 650)
save_fig(
    fig, path.join(base_path, save_dir), "Corr_peak_exp_all", format=save_format,
)


###
# 2) Restrict analysis to single regions
###

for i, reg in enumerate(df_aper.region.unique()):

    # Onset
    fig, ax = plt.subplots(1, 1, figsize=[5, 5])
    ax = plot_corr.plot(
        ax,
        df_data["exp"][df_data.region == reg],
        df_data.onset[df_data.region == reg],
        df_fit=df_test_onset.loc[reg],
        xy_annot=(0.7, 0.05),
        pcorr=True,
        ylabel="Auditory iERP Onset [ms]",
        xlabel="Baseline exponent [a.u.]",
        xticks=np.arange(1, 7, 1),
        yticks=np.arange(0, 601, 100),
        c=color.cycle[reg],
    )
    ax.set_ylim(0, 650)
    save_fig(
        fig,
        path.join(base_path, save_dir),
        "Corr_onset_exp_" + reg,
        format=save_format,
    )

    # Peak
    fig, ax = plt.subplots(1, 1, figsize=[5, 5])
    ax = plot_corr.plot(
        ax,
        df_data["exp"][df_data.region == reg],
        df_data.peak[df_data.region == reg],
        df_fit=df_test_peak.loc[reg],
        xy_annot=(0.7, 0.05),
        pcorr=True,
        ylabel="Auditory iERP Peak [ms]",
        xlabel="Baseline exponent [a.u.]",
        xticks=np.arange(1, 7, 1),
        yticks=np.arange(0, 601, 100),
        c=color.cycle[reg],
    )
    ax.set_ylim(0, 650)
    save_fig(
        fig, path.join(base_path, save_dir), "Corr_peak_exp_" + reg, format=save_format,
    )

# Restore params
reset_default_rc()
