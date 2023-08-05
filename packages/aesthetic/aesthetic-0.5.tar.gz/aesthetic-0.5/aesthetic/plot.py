"""
Plotting utilities that I re-use.

Contents:
    set_style
    set_style_grid
    savefig
    format_ax
"""
import numpy as np, matplotlib.pyplot as plt, pandas as pd
from datetime import datetime

def set_style(stylelist=['science']):
    """
    Set styles using https://github.com/garrettj403/SciencePlots

    Allowed in list:
        'science', 'grid', 'ieee', 'scatter', 'notebook', 'no-latex',
        'dark_background' + any matplotlib default styles (seaborn, etc).

    Color cycles:
        'high-vis', 'bright', 'vibrant', 'muted', 'retro'.
    """
    if isinstance(stylelist, str): stylelist = [stylelist]
    plt.style.use(stylelist)


def set_style_grid(stylelist=['science','notebook','grid']):
    # Utility function for plots with grids.
    set_style(stylelist)


def set_style_scatter(stylelist=['science','notebook','scatter']):
    # Utility function for scatter plots.
    set_style(stylelist)


def savefig(fig, figpath, writepdf=True, dpi=450):
    fig.savefig(figpath, dpi=dpi, bbox_inches='tight')
    print(f'{datetime.utcnow().isoformat()}: made {figpath}')

    if writepdf:
        pdffigpath = figpath.replace('.png','.pdf')
        fig.savefig(pdffigpath, bbox_inches='tight', dpi=dpi, pad_inches=0.05)
        print(f'{datetime.utcnow().isoformat()}: made {pdffigpath}')

    plt.close('all')


def format_ax(ax):
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.get_yaxis().set_tick_params(which='both', direction='in')
    ax.get_xaxis().set_tick_params(which='both', direction='in')
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize('small')
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize('small')
