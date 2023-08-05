from rich.console import Console, Group
from rich.padding import Padding
from textual.app import App
from textual.widgets import ScrollView

from goatpie import GoatPie
from goatpie.components import GoatBar
from goatpie.helpers import data2table


class GoatPieApp(App):
    """
    'Goatcounter' analytics at your fingertips
    """

    # 'GoatPie' instance
    obj: GoatPie

    # Show last XY entries
    limit: int

    async def on_load(self) -> None:
        """
        Bind keys

        :param event: textual.events.Load

        :return: None
        """

        await self.bind("q", "quit", "Quit application")

        # Since 'arrow up' & 'arrow down' work out-of-the-box,
        # binding keys to quit the application suffices for now

    async def on_mount(self) -> None:
        """
        Load widgets

        :return: None
        """

        # Plot visits & pageviews
        plot = GoatBar(self.obj, limit=self.limit)

        # Retrieve data
        referrers = self.obj.get_referrers()
        pages = self.obj.get_pages()
        browsers = self.obj.get_browsers()
        systems = self.obj.get_systems()
        devices = self.obj.get_devices()
        countries = self.obj.get_countries()

        # Create tables from it & group them together
        tables = Group(
            Padding(data2table(referrers, None)),
            Padding(data2table(pages, None)),
            Padding(data2table(browsers, None)),
            Padding(data2table(systems, None)),
            Padding(data2table(devices, None)),
            Padding(data2table(countries, None)),
        )

        # Query console
        console = Console()

        if console.width < 90:
            # Build scrollable view from plot & data tables
            scroll_view = ScrollView(Group(plot, tables))

            # Focus it (enabling 'arrow up/down')
            await self.set_focus(scroll_view)

            # Assign widgets
            await self.view.dock(scroll_view, edge="top")

        else:
            # Build scrollable view from data tables
            table_view = ScrollView(Padding(tables, (1, 0, 0, 0)))

            # Focus it (enabling 'arrow up/down')
            await self.set_focus(table_view)

            # Assign widgets
            await self.view.dock(plot, edge="left", size=int(console.width * 3 / 5))
            await self.view.dock(table_view, edge="right")
