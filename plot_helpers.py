"""Ready-made plots for the NumPy series, so notebooks only need one line per figure.

    from plot_helpers import plot_frame, plot_light_curve

    plot_frame(cube[0])                      # one image of the star
    plot_frame(cube[0], mask=mask)           # ...with the star's pixels outlined
    plot_frame(cube[0], highlight=(5, 5))    # ...with one pixel (row, column) marked in red
    plot_light_curve(time, light_curve)      # brightness over time

Every function draws and shows the figure; nothing needs to be returned or saved.
Colors follow the Datos de Ciencia palette.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, to_rgba

PALETTE = {
    "bg": "#0D1117",
    "orange": "#E85D24",
    "amber": "#F5A623",
    "yellow": "#FCDE5A",
    "white": "#FFFFFF",
    "gray": "#334155",
}

# Semi-transparent red used only to point at specific pixels
HIGHLIGHT = "#FF3B30"

# One hue, dark to light: brighter pixels look brighter on screen
_BRIGHTNESS_CMAP = LinearSegmentedColormap.from_list(
    "brightness", ["#1F0F08", PALETTE["orange"], "#FBD9CB"]
)
_BRIGHTNESS_CMAP.set_bad(PALETTE["gray"])  # NaN pixels show as flat gray


def _style(fig, ax, title, xlabel, ylabel):
    fig.set_facecolor(PALETTE["bg"])
    ax.set_facecolor(PALETTE["bg"])
    ax.set_title(title, color=PALETTE["white"], fontsize=13)
    ax.set_xlabel(xlabel, color=PALETTE["white"], fontsize=11)
    ax.set_ylabel(ylabel, color=PALETTE["white"], fontsize=11)
    ax.tick_params(colors=PALETTE["white"])
    for spine in ax.spines.values():
        spine.set_color(PALETTE["gray"])


def plot_frame(frame, mask=None, highlight=None, title="One frame"):
    """Show a 2D image (H, W).

    mask: boolean array of the same shape; its pixels are outlined in white.
    highlight: one (row, column) pair, or a list of them; those pixels are covered in semi-transparent red.
    """
    frame = np.asarray(frame)
    fig, ax = plt.subplots(figsize=(5, 4.5))
    image = ax.imshow(frame, cmap=_BRIGHTNESS_CMAP)
    _style(fig, ax, title, "Column", "Row")

    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label("Brightness", color=PALETTE["white"])
    colorbar.ax.tick_params(colors=PALETTE["white"])
    colorbar.outline.set_edgecolor(PALETTE["gray"])

    if mask is not None:
        # Draw each edge of a masked pixel that borders a pixel outside the mask
        mask = np.asarray(mask, dtype=bool)
        padded = np.pad(mask, 1)
        for row, col in zip(*np.nonzero(mask)):
            r, c = row + 1, col + 1
            if not padded[r - 1, c]:
                ax.plot([col - 0.5, col + 0.5], [row - 0.5, row - 0.5], color=PALETTE["white"], lw=2)
            if not padded[r + 1, c]:
                ax.plot([col - 0.5, col + 0.5], [row + 0.5, row + 0.5], color=PALETTE["white"], lw=2)
            if not padded[r, c - 1]:
                ax.plot([col - 0.5, col - 0.5], [row - 0.5, row + 0.5], color=PALETTE["white"], lw=2)
            if not padded[r, c + 1]:
                ax.plot([col + 0.5, col + 0.5], [row - 0.5, row + 0.5], color=PALETTE["white"], lw=2)

    if highlight is not None:
        pixels = [highlight] if np.ndim(highlight) == 1 else highlight
        for row, col in pixels:
            # Semi-transparent red fill plus a solid red border, so it stands out on the orange colormap
            ax.add_patch(plt.Rectangle(
                (col - 0.5, row - 0.5), 1, 1,
                facecolor=to_rgba(HIGHLIGHT, 0.45), edgecolor=HIGHLIGHT, lw=2.5,
            ))

    plt.show()


def plot_light_curve(time, brightness, title="Light curve", ylabel="Brightness"):
    """Plot one brightness value per frame against time in days. NaN values are left as gaps."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time, brightness, ".", ms=3, color=PALETTE["orange"])
    _style(fig, ax, title, "Time [days]", ylabel)
    ax.grid(color=PALETTE["gray"], lw=0.5, alpha=0.5)
    plt.show()
