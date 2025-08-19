import datetime
import typer
from cli.utils import set_ui_layout

app = typer.Typer(
    name="DataChain",
    help="DataChain CLI: Multi-Modal Data Transformation Framework",
    add_completion=True,  # Enable shell completion
)

def run_data_chain():
    """Run the DataChain CLI application."""
    set_ui_layout()  # Set the UI layout before starting the application

    # Add your main logic here

@app.command()
def data_chain():
    run_data_chain()

if __name__ == "__main__":
    app()
