import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


from .plot_helpers import get_lims, get_lims_ticks, format_spines, color, fsize

np.random.seed(0)

###
# Parameters
###

# Define order for comparing brain regions (empty strings are created for separations)
RegionsDefaultOrder = [
    "Transverse",
    "",
    "Superior",
    "",
    "Middle",
    "",
    "Inferior",
    "",
    "Insula",
    "",
    "Pole",
]

# Scatter parameters
jitter = 0.15
point_displ = 0.3  # displacement of dots relative to distribution
point_size = 5


def plot(
    ax,
    data,
    y,
    show_medians=True,
    means_prec=1,
    title=None,
    ylabel=None,
    yscale=(None, None),
    yticks=None,
):
    """Scatter plots showing raw data.

    Parameters
    ----------
    ax : Matplotlib's Axes object
        Axes object to plot on. Required.
    data : pandas Dataframe
        Dataframe with channels, regions and parameter values. Required.
    y : str
        Name of column in data to plot. Required.
    show_medians : bool
        Plot median values on top of the distributions. Default True.
    means_prec : str or int
        Precision to use to show median values. Default to 1.
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
    palette = [
        color.cycle[r] if r == "" else color.cycle["subregs"]
        for r in RegionsDefaultOrder
    ]

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
    for dots in ax.collections[::2]:
        dots.set_offsets(dots.get_offsets() + np.array([point_displ, 0]))

    old_len_collections = len(ax.collections)

    if show_medians:
        # Print mean value for every region
        for i, lab in enumerate(ax.get_xticklabels()[::2]):
            # Get x coordinate and text
            x_reg = lab._x
            reg = lab._text
            y_reg = data[y][data.region == reg].max() * 1.03
            med = data[y][data.region == reg].median()
            # Add marker
            ax.scatter(x_reg - 0.1, med, marker="^", s=60, c="k")
            # Add text
            ax.text(
                x_reg,
                y_reg,
                f"{med:.{means_prec}f}",
                weight="bold",
                ha="center",
                va="center",
                fontsize=fsize.MEANS_SIZE+2,
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
