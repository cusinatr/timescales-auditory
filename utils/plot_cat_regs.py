import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


from .plot_helpers import get_lims, get_lims_ticks, format_spines, color, fsize

np.random.seed(0)

###
# Parameters
###

# Define order for comparing brain regions (empty strings are created for separations)
RegionsDefaultOrder = ["CTX", "", "ENT", "", "HIP", "", "AMY"]

# Scatter parameters
jitter = 0.15
point_displ = 0.3  # displacement of dots relative to distribution
point_size = 5


def plot(
    ax,
    data,
    y,
    show_means=True,
    means=None,
    SEMs=None,
    means_prec=1,
    cut=0,
    title=None,
    ylabel=None,
    yscale=(None, None),
    yticks=None,
):
    """Raincloud plots showing distributions and raw data.

    Parameters
    ----------
    ax : Matplotlib's Axes object
        Axes object to plot on. Required.
    data : pandas Dataframe
        Dataframe with channels, regions and parameter values. Required.
    y : str
        Name of column in data to plot. Required.
    show_means : bool
        Plot mean values +- SEM on top of the distributions. Default True.
    means : list
        If provided, display these mean values.
    SEMs : list
        If provided, display these SEM values.
    means_prec : str or int
        Precision to use to show mean values. Default to 1.
    cut : float
        If given, value to cut the data in the distribution plot.
    title : string
        Title of plot. Preferred over ch_name as title if specified.
    ylabel : string
        Label to use on the Y axis.
    yscale : tuple
        (min, max) values for y axis. Default to (None, None),
        in which case the data range is taken.
    yticks : int or float
        If given, specify spacing between ticks.

    Returns
    -------
    ax : Matplotlib's Axes object
        Modified Axes instance.
    """

    # Take color palette
    palette = [color.cycle[r] for r in RegionsDefaultOrder]

    # Violin plot
    sns.violinplot(
        x="region",
        y=y,
        data=data,
        inner=None,
        bw=0.5,
        cut=cut,
        linewidth=1.0,
        dodge=False,
        width=1.0,
        palette=palette,
        order=RegionsDefaultOrder,
        ax=ax,
    )
    for violin in ax.collections:
        bbox = violin.get_paths()[0].get_extents()
        x0, y0, width, height = bbox.bounds
        violin.set_clip_path(
            plt.Rectangle((x0, y0), width / 2, height, transform=ax.transData)
        )

    # Boxplot
    sns.boxplot(
        x="region",
        y=y,
        data=data,
        saturation=1,
        width=0.12,
        linewidth=0.4,
        showfliers=False,
        boxprops={"zorder": 3, "facecolor": "none"},
        dodge=False,
        order=RegionsDefaultOrder,
        ax=ax,
    )

    old_len_collections = len(ax.collections)
    displacement = point_displ

    # Stripplot
    sns.stripplot(
        x="region",
        y=y,
        data=data,
        jitter=jitter,
        size=point_size,
        facecolor="none",
        dodge=False,
        palette=palette,
        order=RegionsDefaultOrder,
        ax=ax,
    )

    # Format dots
    for dots in ax.collections[old_len_collections:][::2]:
        dots.set_offsets(dots.get_offsets() + np.array([displacement, 0]))

    old_len_collections = len(ax.collections)

    if show_means:
        # Print mean value for every region
        for i, lab in enumerate(ax.get_xticklabels()[::2]):
            # Get x coordinate and text
            x_reg = lab._x
            reg = lab._text
            y_reg = data[y][data.region == reg].max() * 1.03
            if means is None:
                mean = data[y][data.region == reg].mean()
            else:
                mean = means[i]
            if SEMs is None:
                sem = data[y][data.region == reg].sem()
            else:
                sem = SEMs[i]
            # Add text
            ax.text(
                x_reg,
                y_reg,
                f"{mean:.{means_prec}f} $\pm$ {sem:.{means_prec}f}",
                weight="bold",
                ha="center",
                va="center",
                fontsize=fsize.MEANS_SIZE,
                clip_on=True,
            )

    # X-axis
    ax.set_xticks(np.arange(0, len(RegionsDefaultOrder), 2))
    ax.set_xticklabels(RegionsDefaultOrder[::2])
    ax.set_xlim(ax.get_xlim()[0] - 0.7, ax.get_xlim()[1] + 0.7)

    # Y-axis
    ylims = ax.get_ylim()
    y_min, y_max = get_lims(ylims, yscale)
    # y_min, y_max, y_ticks = get_lims_ticks(y_min, y_max, yticks)
    y_ticks = get_lims_ticks(y_min, y_max, yticks)
    ax.set_ylim(y_min, y_max)
    ax.set_yticks(y_ticks)

    # Set ticks size
    ax.tick_params(axis="y", which="major", labelsize=fsize.TICK_SIZE)
    ax.tick_params(axis="x", which="major", labelsize=fsize.TICK_SIZE + 2)

    # Axes labels
    ax.set_xlabel("")
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=fsize.LABEL_SIZE)
    else:
        ax.set_ylabel("")

    # Set title if specified.
    if title is not None:
        ax.set_title(title, fontsize=fsize.TITLE_SIZE)

    # Set right and top spines to not visible
    format_spines(ax)

    return ax
