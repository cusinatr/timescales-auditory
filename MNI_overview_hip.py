"""
Plot overview of electrodes in MNI space in HIPPOCAMPUS & AMYGDALA.

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
surf_name = "Hip_Amy.surf.gii"
save_dir = "MNI/HipAmy"
save_format = "svg"

Regions = ["AMY", "HIP"]
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

fig_glass = plt.figure(figsize=[4, 4])
ax_glass = fig_glass.add_subplot(111, projection="3d")
ax_glass = plot_mni_overview(
    ax_glass, surf, df_mni, marker_size=50, elev=45, azim=165, shrink_x=0.5, alpha=0.1,
)

# Save figure
save_fig(
    fig_glass, path.join(base_path, save_dir), "MNI_overview_HIP", format=save_format,
)


# Restore params
reset_default_rc()
