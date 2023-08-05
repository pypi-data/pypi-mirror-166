from rich.padding import Padding
from rich.panel import Panel
from textual.widget import Widget

from .plotext import plotextRenderable


class GoatBar(Widget):
    """
    Textual widget for 'multiple_bar' plot created with 'plotext'
    """

    def __init__(self, obj, limit: int, step: int, bar_colors: list) -> None:
        """
        Initializes 'GoatBar' instance

        :param obj: goatpie.GoatPie
        :param limit: int Bar colors
        :param step: int Limits data being displayed
        :param bar_colors: list Steps used on Y-axis

        :return: None
        """

        # Initialize parent
        super().__init__("GoatBar")

        # Set plotter & settings
        self.obj = obj
        self.limit = limit
        self.step = step
        self.bar_colors = bar_colors

    def render(self) -> Panel:
        """
        Renders 'multiple_bar' plot created with 'plotext'

        :return: rich.panel.Panel
        """

        # Create 'rich' element
        renderable = plotextRenderable(self.obj, self.limit, self.step, self.bar_colors)

        # Define top padding
        spacing = (1, 0, 0, 0)

        return Padding(Panel(renderable, title=f"Last {self.limit} days", padding=spacing), spacing)

    # FIX: Update data & rerender
    # async def update(self, renderable: RenderableType) -> None:
    #     self.renderable = renderable
    #     self.refresh()
