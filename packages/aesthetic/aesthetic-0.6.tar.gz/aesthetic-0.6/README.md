# a e s t h e t i c

Style-related tools that I re-use across projects in astronomy.

Most relevant are the style sheets, which produce default plots as in the
`/results/` directory.

__install__

_Option 1_: `pip install aesthetic`

_Option 2_: Clone + `python setup.py install` from the repo. (or develop!)

__contents__

`aesthetic.plot`
* `set_style`
* `set_style_scatter`
* `savefig`
* `format_ax`

`aesthetic.paper`
* `abbreviate_the_bibliography`

__usage examples__

for plot styles, see the [test driver](https://github.com/lgbouma/aesthetic/blob/master/tests/make_test_plot.py).
the general syntax follows:

```
from aesthetic.plot import set_style
set_style("science")
```

<img src="https://github.com/lgbouma/aesthetic/blob/master/results/plot_science.png" width="500">

```
set_style("clean")
```

<img src="https://github.com/lgbouma/aesthetic/blob/master/results/plot_clean.png" width="500">
