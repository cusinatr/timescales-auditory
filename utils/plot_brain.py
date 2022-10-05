import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors
from utils.plot_helpers import color


def plot_chans_on_surf(
    ax,
    surf,
    Coords,
    param_data,
    cmap_name,
    marker_size=30,
    vmin=None,
    vmax=None,
    azim=140.0,
    elev=0.0,
    shrink_x=1,
    shrink_y=1,
    shrink_z=1,
    dist=10,
    alpha=0.04,
    add_colorbar=False,
    lognorm=False,
):
    """Plot a semi-transparent surface with electrodes (dots) on top,
     colored based on a gradient of parameter's values.

    Args:
        ax (plt.Axes): Axes object to plot on.
        surf: surface object.
        Coords (np.ndarray): (N,3) array with electrodes' MNI coordinates.
        param_data (list-like): parameter value for each electrode.
        cmap_name (string): name of matplotlib's colormap.
        marker_size (int, optional): size (in points) of markers. Defaults to 30.
        vmin (float, optional): If given, minimum value of the colormapto use. Defaults to None.
        vmax (float, optional): If given, maximum value of the colormapto use. Defaults to None.
        azim (float, optional): x-y plane initialization angle. Defaults to 140.0.
        elev (float, optional): z axis initialization angle. Defaults to 0.0.
        shrink_x (int, optional): shrink factor for x coordinate. Defaults to 1.
        shrink_y (int, optional): shrink factor for y coordinate. Defaults to 1.
        shrink_z (int, optional): shrink factor for z coordinate. Defaults to 1.
        dist (int, optional): Distance of view (lower -> more zoomed). Defaults to 10.
        alpha (float, optional): Tranparency value for surface. Defaults to 0.04.
        add_colorbar (bool, optional): If True, add colorbar to plot. Defaults to False.
        lognorm (bool, optional): If True, values of parameter are in log scale. Defaults to False.

    Returns:
        plt.Axes: modified Axes with plotted objects.
    """

    # Shrink axes if values are given
    ax.get_proj = lambda: np.dot(
        Axes3D.get_proj(ax), np.diag([shrink_x, shrink_y, shrink_z, 1])
    )

    # Surface "shadow"
    ax.plot_trisurf(
        surf.coordinates[:, 0],
        surf.coordinates[:, 1],
        surf.faces,
        surf.coordinates[:, 2],
        color="lightgrey",
        alpha=alpha,
    )

    if lognorm:
        norm = colors.LogNorm(vmin=vmin, vmax=vmax)
    else:
        norm = colors.Normalize(vmin=vmin, vmax=vmax)

    p = ax.scatter3D(
        Coords[:, 0],
        Coords[:, 1],
        zs=Coords[:, 2],
        c=param_data,
        cmap=cmap_name,
        s=marker_size,
        depthshade=False,
        alpha=0.6,
        norm=norm,
        linewidth=0
    )

    # Adjust the initial angles of the plot
    ax.view_init(azim=azim, elev=elev)

    # Adjust viewing "distance" of the plot
    ax.dist = dist

    # Make the panes transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # Make the grid lines transparent
    ax.xaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)
    ax.yaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)
    ax.zaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)
    # Set axes off
    ax.set_axis_off()

    if add_colorbar:
        return ax, p

    return ax


def plot_mni_overview(
    ax,
    surf,
    df_plot,
    marker_size=30,
    azim=140.0,
    elev=0.0,
    shrink_x=1,
    shrink_y=1,
    shrink_z=1,
    dist=10,
    alpha=0.04,
):
    """_summary_

    Args:
        ax (plt.Axes): Axes object to plot on.
        surf: surface object.
        df_plot (pd.Dataframe): dataframe containing MNI coordinates, alpha and responsiveness of each electrode.
        marker_size (int, optional): size (in points) of markers. Defaults to 30.
        azim (float, optional): x-y plane initialization angle. Defaults to 140.0.
        elev (float, optional): z axis initialization angle. Defaults to 0.0.
        shrink_x (int, optional): shrink factor for x coordinate. Defaults to 1.
        shrink_y (int, optional): shrink factor for y coordinate. Defaults to 1.
        shrink_z (int, optional): shrink factor for z coordinate. Defaults to 1.
        dist (int, optional): Distance of view (lower -> more zoomed). Defaults to 10.
        alpha (float, optional): Tranparency value for surface. Defaults to 0.04.

    Returns:
        plt.Axes: modified Axes with plotted objects.
    """

    # Shrink axes if values are given
    ax.get_proj = lambda: np.dot(
        Axes3D.get_proj(ax), np.diag([shrink_x, shrink_y, shrink_z, 1])
    )

    # Surface "shadow"
    ax.plot_trisurf(
        surf.coordinates[:, 0],
        surf.coordinates[:, 1],
        surf.faces,
        surf.coordinates[:, 2],
        color="lightgrey",
        alpha=alpha,
    )

    # Separate responsive and non-responsive plots
    df_plot_noresp = df_plot[df_plot.resp == 0].copy()
    p_colors = [color.cycle[r] for r in df_plot_noresp.loc[:, "region"].to_numpy()]
    ax.scatter3D(
        df_plot_noresp.loc[:, "mni_x"].to_numpy(),
        df_plot_noresp.loc[:, "mni_y"].to_numpy(),
        zs=df_plot_noresp.loc[:, "mni_z"].to_numpy(),
        c=p_colors,
        s=marker_size,
        depthshade=False,
        alpha=0.6,
        linewidth=0
    )

    # Then, responsive ones, with edges
    df_plot_resp = df_plot[df_plot.resp == 1].copy()
    p_colors = [color.cycle[r] for r in df_plot_resp.loc[:, "region"].to_numpy()]
    ax.scatter3D(
        df_plot_resp.loc[:, "mni_x"].to_numpy(),
        df_plot_resp.loc[:, "mni_y"].to_numpy(),
        zs=df_plot_resp.loc[:, "mni_z"].to_numpy(),
        c=p_colors,
        s=marker_size,
        depthshade=False,
        alpha=0.6,
        linewidth=1,
        edgecolor='k'
    )

    # Adjust the initial angles of the plot
    ax.view_init(azim=azim, elev=elev)

    # Adjust viewing "distance" of the plot
    ax.dist = dist

    # Make the panes transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # Make the grid lines transparent
    ax.xaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)
    ax.yaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)
    ax.zaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)
    # Set axes off
    ax.set_axis_off()

    return ax
