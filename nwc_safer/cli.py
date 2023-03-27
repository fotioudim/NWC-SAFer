import typer
from pathlib import Path
from rich import print
from typing import List, Tuple
from typing import Optional
from .watcher import Watcher
from .processor import Processor
from .product import Product
from importlib.metadata import version  


app = typer.Typer(no_args_is_help=True)


def file_format_types():
    """
    Supported output file formats by the application
    """
    return ["csv", "xlsx", "txt"]


def file_format_callback(value: str):
    """
    Check if the option parameter provided is amongst the supported output file formats
    """
    if value not in file_format_types():
        raise typer.BadParameter(f"Only {', '.join(file_format_types())} file formats are allowed!")
    return value


def version_callback(value: bool):
    """
    Print the application version in the console
    """
    if value:
        print(f"NWC-SAFer CLI Version: {version('nwc-safer')}")
        raise typer.Exit()
    

@app.callback()
def callback(ctx: typer.Context,
             version: Optional[bool] = typer.Option(None, "--version", "-v", 
                                                    help="Show the application version", callback=version_callback)):
    """
    NWC-SAFer CLI tool --> NWC-SAF NetCDF data exporting and conversion made simple!
    """


@app.command()
def watch(input_path: Path = typer.Argument(".", help="The path (relative/absolute) for the directory desired to be watched",
                                            exists=True, file_okay=False, resolve_path=True),
          output_path: Path = typer.Argument(".\\output\\", help="The path (relative/absolute) for the output directory",
                                             file_okay=False, resolve_path=True),
          lat_bounds: Tuple[int, int] = typer.Option((None, None), "--lat", "-la", 
                                help="The latitude coordinate range in ascending order, given in the form of two int values (min & max)"),
          lon_bounds: Tuple[int, int] = typer.Option((None, None), "--lon", "-lo", 
                                help="The longitude coordinate range in ascending order, given in the form of two int values (min & max)"),
          output_format: str = typer.Option("csv", "--format", "-f", help="The output file format", 
                                            callback=file_format_callback, autocompletion=file_format_types),
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
            recursive, existing_files, lat_bounds, lon_bounds).run()


@app.command()
def convert(file_paths: List[Path] = typer.Argument(None, help="The path(s) (relative/absolute) for the file(s) desired to be converted",
                                             exists=True, dir_okay=False, resolve_path=True),
            output_path: Path = typer.Option(".\\output\\", "--output", "-o", help="The path (relative/absolute) for the output directory",
                                               file_okay=False, resolve_path=True),
            lat_bounds: Tuple[int, int] = typer.Option((None, None), "--lat", "-la", 
                                help="The latitude coordinate range in ascending order, given in the form of two int values (min & max)"),
            lon_bounds: Tuple[int, int] = typer.Option((None, None), "--lon", "-lo", 
                                help="The longitude coordinate range in ascending order, given in the form of two int values (min & max)"),
            output_format: str = typer.Option("csv", "--format", "-f", help="The output file format", 
                                              callback=file_format_callback, autocompletion=file_format_types)):
    """
    Process a single or multiple NWC-SAF NetCDF file(s), by extracting the desired data
    and exporting them in a new file format (eg. Csv, Excel, Plain text)
    """
    if not file_paths:
        raise typer.BadParameter("Missing value for '[FILE_PATHS]...'!")

    for file_path in file_paths:
        Processor().convert(file_path, output_path, output_format, lat_bounds, lon_bounds)


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
    print(":rocket: [bright_cyan]Launched[/bright_cyan] NWC-SAF NetCDF Data Exporter Github repository")
    typer.launch("https://github.com/fotioudim/nwc-safer")
