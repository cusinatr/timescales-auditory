import numpy as np
from .plot_helpers import get_lims, format_spines, color, fsize


def plot(
    ax,
    x,
    df_mean,
    df_sem,
    add_sign=True,
    sign_blocks=None,
    annotate_sign=False,
    xticks=None,
    yticks=None,
    logx=False,
    logy=False,
    title=None,
    xlabel="",
    ylabel="",
    linewidth=3.0,
):
    """Plot showing 'sequential' data for multiple regions.

    Parameters
    ----------
    ax : Matplotlib's Axes object
        Axes object to plot on. Required.
    x : array-like
        'steps' on the x-axis. Required.
    df_mean : DataFrame
        Dataframe specifying the mean values for every step in each region. Required.
    df_sem : DataFrame
        Dataframe specifying the SEM values for every step in each region. Required.
    add_sign : bool
        If True (Default), add bars indicating significant differences.
    sign_blocks : list or None
        List of lists of indexes containing start and end of significant blocks.
    annotate_sign : bool
        If True (Default), add 'step' values nearby blocks start/end.
    xticks : array-like
        Ticks to put on y-axis. If None, produce them.
    yticks : array-like
        Ticks to put on y-axis. If None, produce them.
    logx : bool
        If True, draw xticks in log space. Default to False.
    logy : bool
        If True, draw yticks in log space. Default to False.
    title : str
        Title of the plot.
    xlabel : str
        Label of x-axis.
    ylabel : str
        Label of y-axis.
    linewidth : float
        Width of plotted lines.

    Returns
    -------
    ax : Matplotlib's Axes object
        Modified Axes instance.
    """

    # Store max value of the plot
    max_val = np.max(df_mean.to_numpy())

    Regions = df_mean.columns
    for reg in Regions:

        mean_reg = df_mean[reg]
        sem_reg = df_sem[reg]
        if logy:
            range_low = 10 ** (np.log10(mean_reg) - np.log10(sem_reg))
            range_high = 10 ** (np.log10(mean_reg) + np.log10(sem_reg))
        else:
            range_low = mean_reg - sem_reg
            range_high = mean_reg + sem_reg

        ax.plot(x, mean_reg, c=color.cycle[reg], lw=linewidth, label=reg)
        ax.fill_between(
            x, range_low, range_high, color=color.cycle[reg], alpha=0.3,
        )

    if add_sign:

        assert sign_blocks is not None, "sign_blocks must be given if add_sign is True!"

        for block in sign_blocks:
            ax.plot(
                [x[block[0]], x[block[1]]],
                [max_val * 1.03, max_val * 1.03],
                c="k",
                lw=1.5,
            )
            if annotate_sign:
                ax.annotate(
                    f"{x[block[0]]:.0f}",
                    (x[block[0]], max_val),
                    ha="center",
                    fontsize=fsize.TEXT_SIZE,
                )
                ax.annotate(
                    f"{x[block[1]]:.0f}",
                    (x[block[1]], max_val),
                    ha="center",
                    fontsize=fsize.TEXT_SIZE,
                )

    # Add legend
    ax.legend(frameon=False, fontsize=fsize.TEXT_SIZE)

    # Format axes: set limits and ticks
    if logx:
        ax.set_xscale("log")
    xlims = ax.get_xlim()
    # x_ticks = xticks if logx is False else np.log10(xticks)
    x_min, x_max = get_lims(xlims, (xticks[0], xticks[-1]))
    ax.set_xlim(x_min, x_max)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks)

    if logy:
        ax.set_yscale("log")
    ylims = ax.get_ylim()
    # y_ticks = yticks if logy is False else np.log10(yticks)
    y_min, y_max = get_lims(ylims, (yticks[0], yticks[-1]))
    ax.set_ylim(y_min, y_max)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks)

    # Ticks sizes
    ax.tick_params(axis="y", which="major", labelsize=fsize.TICK_SIZE)
    ax.tick_params(axis="x", which="major", labelsize=fsize.TICK_SIZE)

    # Axes labels and title
    ax.set_xlabel(xlabel, fontsize=fsize.LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=fsize.LABEL_SIZE)
    if title is not None:
        ax.set_title(title, fonsize=fsize.TITLE_SIZE)

    # Format spines
    format_spines(
        ax,
        s_bounds={"bottom": (xticks[0], xticks[-1]), "left": (yticks[0], yticks[-1]),},
    )

    return ax
