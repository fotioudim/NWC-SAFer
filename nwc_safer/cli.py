import typer
from pathlib import Path
from rich import print
from .watcher import Watcher
from .processor import Processor
from .product import Product


def output_types():
    return ["csv", "xlsx", "txt"]


app = typer.Typer(no_args_is_help=True)


@app.callback()
def callback(ctx: typer.Context):
    """
    NWC-SAF NetCDF Data Exporter || CLI tool
    """


@app.command()
def watch(input_path: Path = typer.Argument(".", help="The path (relative/absolute) for the directory desired to be watched",
                                            exists=True, file_okay=False, resolve_path=True),
          output_path: Path = typer.Argument(".\output\\", help="The path (relative/absolute) for the output directory",
                                             file_okay=False, resolve_path=True),
          output_format: str = typer.Option("csv", "--format", "-f", help="The output file format", autocompletion=output_types),
          recursive: bool = typer.Option(False, "--recursive", "-r", help="""Watch for incoming files recursively in all
                                                                             the subdirectories of the specified directory"""),
          existing_files: bool = typer.Option(False, "--existing", "-e", help="Convert pre-existing files in the specified directory")):
    """
    Constantly watch a directory for incoming NWC-SAF NetCDF files, in order to
    extract the desired data and export them in the form of Csv/Excel/Text files
    """
    print(":eyes: [light_sky_blue1]Started[/light_sky_blue1] watching for incoming {}files in the '{}' path {}"
          .format("and existing " if existing_files else "", input_path, "recursively" if recursive else ""))
    Watcher(input_path, output_path, output_format,
            recursive, existing_files).run()


@app.command()
def convert(file_path: Path = typer.Argument(..., help="The path (relative/absolute) for the file desired to be converted",
                                             exists=True, dir_okay=False, resolve_path=True),
            output_path: Path = typer.Argument(".\output\\", help="The path (relative/absolute) for the output directory",
                                               file_okay=False, resolve_path=True),
            output_format: str = typer.Option("csv", "--format", "-f", help="The output file format", autocompletion=output_types)):
    """
    Process a single NWC-SAF NetCDF file, by extracting the desired data
    and exporting them in a new file format (eg. Csv, Excel)
    """
    Processor().convert(file_path, output_path, output_format)


@app.command()
def compatibility():
    """
    Check which NWC-SAF products are currently supported
    """
    print(f":ok_hand: [bright_cyan]Supported[/bright_cyan] NWC-SAF products are: [bright_cyan]{', '.join(Product.list())}[/bright_cyan]")


@app.command()
def repo():
    """
    Launch NWC-SAF NetCDF Data Exporter Github repository
    """
    print(
        ":rocket: [bright_cyan]Launched[/bright_cyan] NWC-SAF NetCDF Data Exporter Github repository")
    typer.launch("https://github.com/fotioudim/nwc-safer")
