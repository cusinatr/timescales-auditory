"""
Plot significance levels on top of plots.
"""
import pandas as pd
import numpy as np
import matplotlib.text as mpltext
from utils.plot_helpers import fsize

pval_thre = 0.05
pval_to_asterisks = {1: "n.s.", 0.05: "*", 0.01: "**", 0.001: "***"}


def _get_cat_xy(ax):

    cat_pos = {}
    # Find text objects corresponding to means on display
    texts = ax.findobj(match=mpltext.Text)
    transf = ax.transData.inverted()
    means_coords = [
        (
            t._x,
            t.get_window_extent(ax.figure.canvas.get_renderer()).transformed(transf).y1,
        )
        for t in texts
        if "pm" in t._text  # marks the +- sign of the SEM
    ]

    for cat in ax.get_xticklabels():
        cat_pos[cat._text] = [m for m in means_coords if m[0] == cat._x][0]

    return cat_pos


def _count_bars(p_ovr, p_pairs, write_pairs, write_ns, write_ns_ovr):

    n_sign = 0
    if write_ns_ovr or (p_ovr < pval_thre):
        n_sign += 1
        p_write = {"ovr": p_ovr}
        if write_pairs:
            if write_ns:
                n_sign += len(p_pairs)
                p_write = dict(p_write, **p_pairs)
            else:
                p_pairs_sig = {c: p for c, p in p_pairs.items() if p < pval_thre}
                n_sign += len(p_pairs_sig)
                p_write = dict(p_write, **p_pairs_sig)

    return n_sign, p_write


def _get_text(write_asterisks, pval):

    if write_asterisks:
        for p in sorted(pval_to_asterisks.keys(), reverse=True):
            if pval < p:
                p_sig = p
            else:
                break
        p_text = pval_to_asterisks[p_sig]
    else:
        p_text = f"{pval:.2e}"

    return p_text


def catplot_annot_sign(
    ax,
    df_pval,
    dh=0.03,
    barh=0.01,
    write_pairs=True,
    write_ns=False,
    write_ns_ovr=True,
    write_asterisks=True,
    write_asterisks_ovr=True,
):
    """
    Annotate "Categorical" plots with p-values.

    Parameters
    ----------
    ax : matplotlib Axes object
        Axes on which to plot. Required.
    df_pval : pandas Dataframe
        Dataframe with p-values for "Overall" significance and pairwise comparisons. Required.
    dh : float
        % of the figure height occupied by each horizontal bar.
    barh : float
        % of the figure occupied by the lateral "ticks" of the bar.
    write_pairs : bool
        (Default : True). Whether to note pairwise comparisons.
    write_ns : bool
        (Default : False). Whether to write non-significant results for comparisons.
    write_ns_ovr : bool
        (Default : True). Whether to write non-significant results for overall.
    write_asterisks : bool
        (Default : True). Whether to write codes corresponsing to p-values or p-values themselves for comparisons.
    write_asterisks_ovr : bool
        (Default : True). Whether to write codes corresponsing to p-values or p-values themselves for overall.
    
    Returns
    -------
    ax : matplotlib Axes object
        Modified Axes object
    """

    # Get axis limits
    ylims = ax.get_ylim()
    ywidth = ylims[1] - ylims[0]

    # "Stretch" everything by limits
    dh *= ywidth
    barh *= ywidth

    # Set index if needed
    if "Comparisons" in df_pval.columns:
        df_pval.set_index("Comparisons", inplace=True)

    ###
    # Get x and y coordinates of the categories
    ###

    cat_pos = _get_cat_xy(ax)

    # Format data between "Overall" and "Pairwise" comparisons
    p_ovr = float(df_pval.loc["Overall"].pvalue)
    p_pairs = df_pval.iloc[1:].to_dict()["pvalue"]

    # "Count" how many spaces are needed
    n_sign, p_write = _count_bars(p_ovr, p_pairs, write_pairs, write_ns, write_ns_ovr)

    # If no plotting, return axis as is
    if n_sign == 0:
        return ax

    ###
    # "Overall" plotting
    ###
    y_max = max([p[1] for p in cat_pos.values()])
    if (ylims[1] - y_max) < 2 * n_sign * dh:
        ax.set_ylim(ylims[0], y_max + 2 * n_sign * dh)

    x_min = min([p[0] for p in cat_pos.values()])
    x_max = max([p[0] for p in cat_pos.values()])

    deltah = 2 * (n_sign - 1) * dh + dh
    ovr_txt = _get_text(write_asterisks_ovr, p_write["ovr"])
    ax.plot([x_min, x_max], [y_max + deltah, y_max + deltah], c="k", lw=1.0)
    ax.text(
        (x_max + x_min) / 2,
        (y_max + deltah),
        ovr_txt,
        ha="center",
        va="bottom",
        fontsize=fsize.TEXT_SIZE,
    )

    if n_sign == 1:
        return ax

    ###
    # Pairwise comparisons plotting
    ###

    i_bar = 0  # keep track of bars plotted
    for comp, p_comp in p_write.items():
        if comp != "ovr":
            # Get categories of comparison
            cat1, cat2 = comp.split(" - ")
            x1 = cat_pos[cat1][0]
            x2 = cat_pos[cat2][0]
            deltah = 2 * i_bar * dh + dh
            y_comp = y_max + deltah
            comp_txt = _get_text(write_asterisks, p_comp)
            ax.plot(
                [x1, x1, x2, x2],
                [y_comp, y_comp + barh, y_comp + barh, y_comp],
                c="k",
                lw=0.6,
            )
            ax.text(
                (x1 + x2) / 2,
                y_comp + barh,
                comp_txt,
                ha="center",
                va="bottom",
                fontsize=fsize.TEXT_SIZE,
            )

            i_bar += 1

    return ax
