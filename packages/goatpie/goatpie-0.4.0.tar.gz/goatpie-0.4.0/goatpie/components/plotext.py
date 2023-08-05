import plotext
from rich.ansi import AnsiDecoder
from rich.console import Console, Group
from rich.jupyter import JupyterMixin


class plotextRenderable(JupyterMixin):
    """
    'Rich' renderable for plots created with 'plotext'
    """

    # Plot contents
    rich_canvas: Group

    def __init__(self, obj, limit: int, step: int, bar_colors: list) -> None:
        """
        Initializes 'plotextRenderable' instance

        :param obj: goatpie.GoatPie
        :param limit: int Limits data being displayed
        :param step: int Steps used on Y-axis
        :param bar_colors: list Bar colors

        :return: None
        """

        # Set plotter & settings
        self.obj = obj
        self.limit = limit
        self.step = step
        self.bar_colors = bar_colors

        # Implement decoder
        self.decoder = AnsiDecoder()

    def __rich_console__(self, console: Console, options: dict) -> None:
        """
        Creates canvas for display in the console

        :param console: Console
        :param options: dict

        :return: None
        """

        # Determine dimensions
        width = options.max_width or console.width
        height = options.height or console.height

        # Create canvas from plotted stats
        canvas = self.render_stats(width, height)
        self.rich_canvas = Group(*self.decoder.decode(canvas))

        yield self.rich_canvas

    def render_stats(self, width: int, height: int) -> str:
        """
        Renders visits & pageviews using 'plotext'

        :param width: int Plot width
        :param height: int Plot height

        :return: str Plotted canvas
        """

        # Clear everything
        plotext.clf()
        plotext.clc()

        # Retrieve data
        visits = self.obj.get_visits(self.limit)
        pageviews = self.obj.get_pageviews(self.limit)

        # Configure plot
        plotext.multiple_bar(
            visits.Day,
            [visits.Visits, pageviews.Pageviews],
            label=["Visits", "Pageviews"],
            width=0.4,
            marker="hd",
            color=self.bar_colors,
        )
        plotext.plotsize(width, height)
        plotext.xlabel("hits / day")
        plotext.frame(False)
        plotext.ticks_color("white")
        plotext.ticks_style("bold")
        plotext.xticks([])
        plotext.yticks(range(0, pageviews.Pageviews.max(), self.step))

        return plotext.build()
