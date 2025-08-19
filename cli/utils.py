
import typer
from rich.panel import Panel
from rich.align import Align
from rich.console import Console

console = Console()

def set_ui_layout():
    """Set user interaction before starting the function."""

    # Display ASCII art welcome message
    with open("./cli/static/welcome.txt", "r") as f:
        welcome_ascii = f.read()

    # Create welcome box content
    welcome_content = f"{welcome_ascii}\n"
    welcome_content += "[bold magenta]DataChain: Multi-Modal Data Transformation Framework - CLI[/bold magenta]\n\n"
    welcome_content += (
        "[dim]Built by [XLab-Open](https://github.com/XLab-Open/Datachain)[/dim]"
    )

    # Create and center the welcome box
    welcome_box = Panel(
        welcome_content,
        border_style="magenta",
        padding=(1, 10),
        title="Welcome to DataChain",
        subtitle="Multi-Modal Data Transformation Framework",
    )
    console.print(Align.center(welcome_box))
    console.print()  # Add a blank line after the welcome box
