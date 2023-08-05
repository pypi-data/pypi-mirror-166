import matplotlib as mpl
import numpy as np, matplotlib.pyplot as plt
from aesthetic.plot import savefig, set_style, format_ax

x = np.linspace(0,10,1000)
y = (x/100)**3 + 5*np.sin(x)

_x, _y = np.arange(2, 8, 0.5), np.arange(2, 8, 0.5)

def do_plot():
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.plot(x, y+3, label='test')
    ax.plot(x, y+6)
    ax.scatter(_x, _y)
    ax.set_xlabel(r'x [units]')
    ax.set_ylabel(r'y [units]')
    ax.legend()
    return fig

set_style('clean')
fig = do_plot()
savefig(fig, '../results/plot_clean.png')
mpl.rc_file_defaults()

set_style('science')
fig = do_plot()
savefig(fig, '../results/plot_science.png')
mpl.rc_file_defaults()

set_style('scatter')
fig = do_plot()
savefig(fig, '../results/plot_scatter.png')
mpl.rc_file_defaults()

set_style('grid')
fig = do_plot()
savefig(fig, '../results/plot_grid.png')
