from os import path, makedirs
import numpy as np
from matplotlib import rcParams, rcParamsDefault
from seaborn import color_palette as cp

# Color palette to use
color_palette = cp("Set2")
color_palette2 = cp("Paired")


class color:
    """Store plots objects' colors"""

    cycle = {
        "CTX": color_palette[3],
        "ENT": color_palette[2],
        "HIP": color_palette[1],
        "AMY": color_palette[0],
        "subregs": color_palette[-1],
        "": (0, 0, 0),
    }
    corr = "tab:purple"
    brown = color_palette[-2]
    yellow = color_palette[-3]
    grey = color_palette[-1]
    blue = color_palette2[1]
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class fsize:
    """Store plots objects' fontsizes"""

    TEXT_SIZE = 12
    MEANS_SIZE = 12
    TITLE_SIZE = 15
    TICK_SIZE = 12
    LABEL_SIZE = 15


###
# Helpers
###


def set_font_params():
    """Set figures font"""

    rcParams["font.family"] = "sans-serif"
    rcParams["font.sans-serif"] = "Arial"
    rcParams["font.weight"] = "regular"


def reset_default_rc():
    rcParams.update(rcParamsDefault)


def format_spines(ax, s_inv=["top", "right"], s_bounds={}):
    """Format axis spines"""

    # Set spines to not visible
    for s in s_inv:
        ax.spines[s].set_visible(False)

    # Put bounds on spines
    for s, b in s_bounds.items():
        ax.spines[s].set_bounds(b[0], b[1])


def get_lims(a_lims, a_scale):
    """Get limits for axis"""

    if a_scale[0] is None:
        a_min = a_lims[0]
    else:
        a_min = min(a_lims[0], a_scale[0] - 1e-10)
    if a_scale[1] is None:
        a_max = a_lims[1]
    else:
        a_max = max(a_lims[1], a_scale[1] + 1e-10)

    return a_min, a_max


def get_lims_ticks(a_min, a_max, a_tick):
    """Set axis ticks based on spacing"""

    if a_tick is None:
        # Set up ticks directly
        a_ticks = np.linspace(a_min, a_max, 5)
    elif isinstance(a_tick, list) or isinstance(a_tick, np.ndarray):
        # If ticks are directly provided, return them
        a_ticks = a_tick.copy()
    else:
        # Find closest multiples of the ticks to min and max
        a_min = round(a_min / a_tick) * a_tick
        a_max = round(a_max / a_tick) * a_tick
        a_ticks = np.arange(a_min, a_max + a_tick, a_tick)

    return a_ticks  # a_min, a_max, a_ticks


def save_fig(fig, save_path, name="Figure", format="svg"):
    """Save Figure instance"""

    # Create folder if not exists
    makedirs(save_path, exist_ok=True)

    fig.savefig(
        path.join(save_path, name + "." + format), format=format, bbox_inches="tight",
    )

