from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()


def show_welcome():

    logo = r"""
██████╗ ███████╗██████╗  ██████╗ ███╗   ███╗██╗███╗   ██╗██████╗
██╔══██╗██╔════╝██╔══██╗██╔═══██╗████╗ ████║██║████╗  ██║██╔══██╗
██████╔╝█████╗  ██████╔╝██║   ██║██╔████╔██║██║██╔██╗ ██║██║  ██║
██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║  ██║
██║  ██║███████╗██║     ╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
╚═╝  ╚══════╝╚═╝      ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝
"""

    console.print(
        Align.center(
            Text(logo, style="bold cyan")
        )
    )

    console.print(
        Align.center(
            "[bold]Welcome to RepoMind[/bold]"
        )
    )

    console.print()

    console.print(
        Align.center(
            "[bold green]✓ Don't forget to add your credentials to the .env file[/bold green]"
        )
    )

    console.print()