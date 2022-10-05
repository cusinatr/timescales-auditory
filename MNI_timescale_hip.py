"""
Plot baseline timescales on electrodes in MNI space in HIPPOCAMPUS & AMYGDALA.
Additionally, correlations between the parameters and the coordinates are performed.

The script reads data contained in the csv file specified by data_file_name,
where the timescale for each channel are already stored and coords_file_name,
where the MNI coordinates for each channel are already stored .
The test_name file allows to run Linear Mixed models tests of significance
for correlations.

The data is then plotted in scatter plots (correlations) of 3d visualisations
with brain templates.
"""

from os import path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from nilearn import surface
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from sklearn.cross_decomposition import PLSRegression

from utils.helpers import get_MNI_params, project_hemis_surf, project_hemis_chans
from utils.plot_brain import plot_chans_on_surf
from utils.R_convert import run_R_test_corr
from utils import plot_corr
from utils.plot_helpers import fsize, save_fig, set_font_params, reset_default_rc

###
# Paths and parameters
###

base_path = ""
data_dir = ""
coords_file_name = ""
data_file_name = ""
surf_dir = "surfaces"
surf_name = "Hip_Amy.surf.gii"
test_dir = "LMEs"
test_name = "LME_corr.R"
save_dir = "MNI/HipAmy"
save_format = "svg"

param = "log_tau"
Regions = ["AMY", "HIP"]
hemisphere = "left"
cmap_name = "hot"  # viridis, copper, afmhot
vmin = 40
vmax = 90
vspace = 10

# Set font parameters for plots
set_font_params()


###
# Load data
###

df_mni = pd.read_csv(path.join(base_path, data_dir, coords_file_name), index_col=0)
df_param = pd.read_csv(path.join(base_path, data_dir, data_file_name), index_col=0)
surf_file = path.join(base_path, data_dir, surf_dir, surf_name)
surf = surface.load_surf_mesh(surf_file)

###
# Compute a single data-frame
###

df_data = get_MNI_params(df_mni, df_param, param)
df_data = df_data[df_data.region.isin(Regions)]
Coords = df_data.loc[:, ["mni_x", "mni_y", "mni_z"]].to_numpy()
param_reg = df_data.loc[:, param].to_numpy()

###
# Keep only one hemisphere
###

surf = project_hemis_surf(surf, hemisphere)
Coords = project_hemis_chans(Coords, hemisphere)
df_data.loc[:, ["mni_x", "mni_y", "mni_z"]] = Coords.copy()

###
# Plot
###

fig_glass = plt.figure(figsize=[4, 4])
ax_glass = fig_glass.add_subplot(111, projection="3d")
ax_glass, p = plot_chans_on_surf(
    ax_glass,
    surf,
    Coords,
    10 ** param_reg,
    cmap_name,
    vmin=vmin,
    vmax=vmax,
    marker_size=50,
    elev=45,
    azim=165,
    shrink_x=0.5,
    alpha=0.1,
    add_colorbar=True,
)

cax = inset_axes(ax_glass, height="2%", width="60%", loc="lower center", borderpad=9)
cbar = fig_glass.colorbar(
    p, cax=cax, format="%d", orientation="horizontal"
)
cbar.set_label(label=r"Baseline $\tau$ [ms]", size=fsize.LABEL_SIZE)
cbar.ax.set_xticks(np.arange(vmin, vmax + vspace, vspace))
cbar.ax.tick_params(axis="x", which="minor", bottom=False, labelbottom=False)
cbar.ax.tick_params(axis="x", which="major", labelsize=fsize.TICK_SIZE)

# Save figure
save_fig(
    fig_glass,
    path.join(base_path, save_dir),
    "MNI_" + param + "_HIP",
    format=save_format,
)

###
# Correlations
###

# Partial Least Squares
pls = PLSRegression(n_components=1)
pls.fit(Coords, param_reg)
df_data["pls_x"] = pls.x_scores_

# Run LME tests
source_path = "./" + test_dir + "/" + test_name
save_path = base_path + save_dir + "/"

df_test_x = run_R_test_corr(
    source_path,
    df_data,
    "mni_x",
    param,
    save_path,
    save_name_add="HIP",
    run_single=False,
)
df_test_y = run_R_test_corr(
    source_path,
    df_data,
    "mni_y",
    param,
    save_path,
    save_name_add="HIP",
    run_single=False,
)
df_test_z = run_R_test_corr(
    source_path,
    df_data,
    "mni_z",
    param,
    save_path,
    save_name_add="HIP",
    run_single=False,
)
df_test_pls = run_R_test_corr(
    source_path,
    df_data,
    "pls_x",
    param,
    save_path,
    save_name_add="HIP",
    run_single=False,
)

# Correct X, Y, Z tests for multiple comparisons
df_test_x.pval *= 3
df_test_y.pval *= 3
df_test_z.pval *= 3

###
# Plots
###

# X coord
fig, ax = plt.subplots(1, 1, figsize=[5, 5])
ax = plot_corr.plot(
    ax,
    df_data.mni_x,
    df_data[param],
    df_fit=df_test_x.iloc[0],
    xy_annot=(0.7, 0.8),
    ylabel=r"Baseline $\tau$ [ms]",
    xlabel="MNI X coordinate [mm]",
    xticks=np.arange(-40, -24, 15),
    yticks=np.arange(vmin, vmax + vspace, vspace),
    logy=True,
    pcorr=True
)
# Add indication of "direction"
xlabs = [l.get_text() for l in ax.get_xticklabels()]
xlabs[0] += "\n" + r"$\bf{Left}$"
xlabs[-1] += "\n" + r"$\bf{Central}$"
ax.set_xticklabels(xlabs, fontsize=fsize.TICK_SIZE)
save_fig(
    fig,
    path.join(base_path, save_dir),
    "Corr_" + param + "_MNIx_HIP",
    format=save_format,
)

# Y coord
fig, ax = plt.subplots(1, 1, figsize=[5, 5])
ax = plot_corr.plot(
    ax,
    df_data.mni_y,
    df_data[param],
    df_fit=df_test_y.iloc[0],
    xy_annot=(0.8, 0.05),
    ylabel=r"Baseline $\tau$ [ms]",
    xlabel="MNI Y coordinate [mm]",
    xticks=np.arange(-50, 11, 20),
    yticks=np.arange(vmin, vmax + vspace, vspace),
    logy=True,
    pcorr=True
)
# Add indication of "direction"
xlabs = [l.get_text() for l in ax.get_xticklabels()]
xlabs[0] += "\n" + r"$\bf{Posterior}$"
xlabs[-1] += "\n" + r"$\bf{Anterior}$"
ax.set_xticklabels(xlabs, fontsize=fsize.TICK_SIZE)
save_fig(
    fig,
    path.join(base_path, save_dir),
    "Corr_" + param + "_MNIy_HIP",
    format=save_format,
)

# Z coord
fig, ax = plt.subplots(1, 1, figsize=[5, 5])
ax = plot_corr.plot(
    ax,
    df_data.mni_z,
    df_data[param],
    df_fit=df_test_z.iloc[0],
    xy_annot=(0.8, 0.8),
    ylabel=r"Baseline $\tau$ [ms]",
    xlabel="MNI Z coordinate [mm]",
    xticks=np.arange(-30, 1, 10),
    yticks=np.arange(vmin, vmax + vspace, vspace),
    logy=True,
    pcorr=True
)
# Add indication of "direction"
xlabs = [l.get_text() for l in ax.get_xticklabels()]
xlabs[0] += "\n" + r"$\bf{Inferior}$"
xlabs[-1] += "\n" + r"$\bf{Superior}$"
ax.set_xticklabels(xlabs, fontsize=fsize.TICK_SIZE)
save_fig(
    fig,
    path.join(base_path, save_dir),
    "Corr_" + param + "_MNIz_HIP",
    format=save_format,
)

# PLS
fig, ax = plt.subplots(1, 1, figsize=[5, 5])
ax = plot_corr.plot(
    ax,
    df_data.pls_x,
    df_data[param],
    df_fit=df_test_pls.iloc[0],
    xy_annot=(0.05, 0.8),
    ylabel=r"Baseline $\tau$ [ms]",
    xlabel="PLS scores",
    xticks=np.arange(-3, 3, 1),
    yticks=np.arange(vmin, vmax + vspace, vspace),
    logy=True,
)
save_fig(
    fig,
    path.join(base_path, save_dir),
    "Corr_" + param + "_PLS_HIP",
    format=save_format,
)

###
# Plot of "direction" of PLS in mni space
###

Coords_pls = pls.inverse_transform(pls.transform(Coords))

ax_glass.plot(
    Coords_pls[:, 0], Coords_pls[:, 1], Coords_pls[:, 2], lw=4.0, c="tab:green"
)
save_fig(
    fig_glass,
    path.join(base_path, save_dir),
    "MNI_" + param + "_HIP_pls",
    format=save_format,
)

# Restore params
reset_default_rc()
