from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()
from repomind.config.config import load_config
config = load_config()
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
        Align.center("[bold purple]👨‍💻 Made by Yadav Nitesh[/]")
    )
    console.print(
        Align.center("[dim]🔗 GitHub:[/] [link=https://github.com/yadavnitesh86][bold cyan]@yadavnitesh86[/][/link]")
    )
    console.print()

    console.print(
    Align.center(
        "[bold green]⚠ This agent requires a Git repository.[/]\n"
        "[dim]Initialize it by running:[/] [bold cyan]git init[/]"
      )
    )
    console.print()

    console.print(
        Align.center(
            "[bold green]✓ Don't forget to add your credentials to the .env file[/bold green]"
        )
    )
    console.print()

    provider = config["ChatGroq"]["provider"]
    model = config["ChatGroq"]["model"]
    console.print(
    f"\n[bold cyan]🤖 Provider:[/bold cyan] [bold green]{provider}[/bold green]"
    f"  [bold cyan]🧠 Model:[/bold cyan] [bold green]{model}[/bold green]\n"
     )