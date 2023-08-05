# GoatPie
[![Build](https://ci.codeberg.org/api/badges/RefBW/goatpie/status.svg)](https://codeberg.org/RefBW/goatpie/issues)

"GoatCounter" analytics for the CLI, written in Python - get it?

![Screenshot](screenshot.png)


## Installation

It's available from [PyPi](https://pypi.org/project/gesetze) using `pip`:

```text
pip install goatpie
```

## Getting started

Using this library is straightforward.


### Commandline

Pretty much self-explanatory - otherwise, `--help` is your friend:

```text
$ goatpie --help
Usage: goatpie [OPTIONS] URL

  Provides 'Goatcounter' statistics for URL

Options:
  -u, --update            Forces update of local database
  -l, --limit INTEGER     Shows visits & pageviews for the last XY days. Default: 14
  -b, --bar-colors TEXT   Defines two bar colors. Default: 'blue,magenta'
  -t, --text-colors TEXT  Defines three text colors. Default: 'blue,white,cyan'
  --version               Show the version and exit.
  --help                  Show this message and exit.
```


### Package

The underlying module may also be used directly:

```python
from goatpie import GoatPie

# Initialize it
obj = GoatPie(url, token)

# Optionally with `data_dir` (SQLite database, config, etc)
obj = GoatPie(url, token, data_dir)

# Update database
# (1) Last update not before one hour (in seconds)
obj.update(3600)

# (2) Force database update
obj.update(0)

# Get pageviews as `pandas.DataFrame` (last seven days)
print(obj.get_pageviews(7))

#           Day  Pageviews
# 0  2022-08-28          1
# 1  2022-08-27         13
# 2  2022-08-26         20
# 3  2022-08-25         35
# 4  2022-08-24         84
# 5  2022-08-23         64
# 6  2022-08-22         23
```


## Configuration

Besides CLI options (see `goatpie --help`) you may also configure various options inside `~/.config/goatpie/config.ini` like so:

```ini
[DEFAULT]
interval = 3600
step = 100
bar_colors = blue,magenta
text_colors = blue,white,cyan

[stats.example.com]
interval = 0                    # force updates
step = 1000                     # more visitors
bar_colors = yellow,red         # hotter colors
text_colors = black,blue,black  # better suited for light screens
```

When first connecting to a 'GoatCounter' domain (such as `stats.example.com`), you are asked to store your token, in which case your configuration might look like this:

```ini
[DEFAULT]
interval = 3600

[stats.example.com]
interval = 0  # force updates
token = my-s3cr3t-t0k3n

[stats.another-example.com]
interval = 1800  # half hour
token = my-0th3r-s3cr3t-t0k3n
```

**Note**: Section headers are named after the GoatCounter API endpoints you are using, NOT the pages you are tracking!


## Roadmap

- [x] Add tests
- [ ] Add more tests
- [x] Add logger
- [x] Config file
- [x] Explain configuration
