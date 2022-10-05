"""
Plot overview of electrodes in MNI space in CORTEX.

The script reads coordinates data contained in the csv file specified by coords_file_name,
where the MNI coordinates for each channel are already stored .

The data is 3d visualisations with brain templates.
"""

from os import path
import matplotlib.pyplot as plt
import pandas as pd
from nilearn import surface

from utils.helpers import project_hemis_surf, project_hemis_chans
from utils.plot_brain import plot_mni_overview
from utils.plot_helpers import save_fig, set_font_params, reset_default_rc

###
# Paths and parameters
###

base_path = ""
data_dir = ""
coords_file_name = ""
surf_dir = "surfaces"
surf_name = "cortex_5124.surf.gii"
save_dir = "MNI"
save_format = "svg"

Regions = ["CTX", "ENT"]
hemisphere = "left"

# Set font parameters for plots
set_font_params()

###
# Load data
###

df_mni = pd.read_csv(path.join(base_path, data_dir, coords_file_name), index_col=0)
surf_file = path.join(base_path, data_dir, surf_dir, surf_name)
surf = surface.load_surf_mesh(surf_file)

df_mni = df_mni[df_mni.region.isin(Regions)]
Coords = df_mni.loc[:, ["mni_x", "mni_y", "mni_z"]].to_numpy()

###
# Keep only one hemisphere
###

surf = project_hemis_surf(surf, hemisphere)
Coords = project_hemis_chans(Coords, hemisphere)
df_mni.loc[:, ["mni_x", "mni_y", "mni_z"]] = Coords.copy()

###
# Plot
###

fig_glass = plt.figure(figsize=[8, 4],)
ax1 = fig_glass.add_subplot(121, projection="3d")
ax1 = plot_mni_overview(ax1, surf, df_mni, marker_size=20, azim=180, elev=0, dist=5.5)

ax2 = fig_glass.add_subplot(122, projection="3d")
ax2 = plot_mni_overview(
    ax2, surf, df_mni, marker_size=20, azim=90, elev=0, shrink_x=0.5, dist=5.5,
)

# Adjust distance between subplots
fig_glass.subplots_adjust(wspace=0, hspace=0)

# Save figure
save_fig(
    fig_glass, path.join(base_path, save_dir), "MNI_overview_CTX", format=save_format,
)

# Restore params
reset_default_rc()
