import numpy as np
from scipy.stats import linregress
from matplotlib import colors, rcParams

from .plot_helpers import get_lims, format_spines, color, fsize

np.random.seed(0)


def plot(
    ax,
    x,
    y,
    compute=False,
    df_fit=None,
    pcorr=False,
    c=color.corr,
    xy_annot=(0.1, 0.85),
    xticks=None,
    yticks=None,
    logx=False,
    logy=False,
    title=None,
    xlabel="",
    ylabel="",
):

    """
    Compute correlation value (optional) and plot it together with scatterplot.

    Parameters
    ----------
    ax : matplotlib Axes object
        Axes on which to plot. Required.
    x : list or ndarray
        x coordinates of points. Required.
    y : list or ndarray
        y coordinates of points. Required.
    compute : bool
        If True, compute the correlation. Default to False.
    df_fit : None or pandas Dataframe
        If given, dataframe with fit info.
    pcorr : bool
        If True, the p-value is corrected for multiple comparisons. Default to False.
    c : str
        Color for plot.
    xy_annot : tuple of 2
        Coordinates in axes space of where to plot the text.
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

    Returns
    -------
    ax : matplotlib Axes object
        Modified Axes.
    """

    # Plot scatter
    ax.scatter(
        x,
        y,
        marker="o",
        edgecolor=c,
        facecolor=colors.to_rgba(c, alpha=0.6),
        linewidth=0.5,
        s=25,
    )

    # Compute regression coefficients
    if compute:
        res = linregress(x, y)
        m = res.slope
        q = res.intercept
        rho = res.rvalue
        pval = res.pvalue
    else:
        assert df_fit is not None, "df_fit need to be given!"
        m = df_fit.m
        q = df_fit.q
        rho = df_fit.rho
        pval = df_fit.pval

    # Values for the x axis
    x_fit = np.linspace(min(x), max(x), 1000)

    # Plot regression line
    ax.plot(x_fit, q + m * x_fit, ls="--", c=c, alpha=0.8, lw=2.5)

    # Annotate regression parameters
    p_str = r"p " if not pcorr else r"p$_{\rm corr}$ "
    p_str += "= " + str(round(pval, 3)) if pval > 0.001 else "< 0.001"
    if pval < 0.05:
        p_str += r" $\bf{*}$"
    ax.annotate(
        r"$\rho$" + " = " + str(round(rho, 3)) + "\n" + p_str,
        xy=xy_annot,
        xycoords="axes fraction",
        fontsize=fsize.TEXT_SIZE,
    )

    # Format axes: set limits and ticks
    xlims = ax.get_xlim()
    x_ticks = xticks if logx is False else np.log10(xticks)
    x_min, x_max = get_lims(xlims, (x_ticks[0], x_ticks[-1]))
    ax.set_xlim(x_min, x_max)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(xticks)

    ylims = ax.get_ylim()
    y_ticks = yticks if logy is False else np.log10(yticks)
    y_min, y_max = get_lims(ylims, (y_ticks[0], y_ticks[-1]))
    ax.set_ylim(y_min, y_max)
    ax.set_yticks(y_ticks)
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
        s_bounds={
            "bottom": (x_ticks[0], x_ticks[-1]),
            "left": (y_ticks[0], y_ticks[-1]),
        },
    )

    return ax
