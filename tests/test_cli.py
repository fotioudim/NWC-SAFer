from typer.testing import CliRunner
from nwc_safer.cli import app
import os.path
import shutil
import pytest

runner = CliRunner()


RESOURCES_DIRECTORY = ".\\resources\\"
OUTPUT_DIRECTORY = ".\\output\\"


@pytest.fixture(scope="session", autouse=True)
def image_file():
    if os.path.isdir(OUTPUT_DIRECTORY):
        shutil.rmtree(OUTPUT_DIRECTORY)
    yield
    if os.path.isdir(OUTPUT_DIRECTORY):
        shutil.rmtree(OUTPUT_DIRECTORY)


def test_app():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "NWC-SAFer CLI tool --> NWC-SAF NetCDF data exporting and conversion made simple!" in result.stdout

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.3.0" in result.stdout

def test_compatibility():
    result = runner.invoke(app, ["compatibility"])
    assert result.exit_code == 0
    assert "NWC GEO Cloud Type Product" in result.stdout
    assert "NWC GEO Cloud Mask Product" in result.stdout

def test_watch_wrong_output():
    result = runner.invoke(app, ["watch", "-f", "test"])
    assert result.exit_code == 2
    assert "Invalid value for '--format' / '-f': Only csv, xlsx, txt file formats are allowed" in result.stdout

def test_conversion_wrong_output():
    result = runner.invoke(app, ["convert", "-f", "test"])
    assert result.exit_code == 2
    assert "Invalid value for '--format' / '-f': Only csv, xlsx, txt file formats are allowed" in result.stdout

def test_conversion_no_file_path():
    result = runner.invoke(app, ["convert"])
    assert result.exit_code == 2
    assert "Missing value for '[FILE_PATHS]...'!" in result.stdout

def test_conversion_file_path_not_exists():
    result = runner.invoke(app, ["convert", "test.nc"])
    assert result.exit_code == 1
    assert "Invalid value for '[FILE_PATHS]...': File 'sda' does not exist." in result.stdout

def test_conversion_file_path_not_exists():
    result = runner.invoke(app, ["convert", "."])
    assert result.exit_code == 2
    assert "Invalid value for '[FILE_PATHS]...': File '.' is a directory." in result.stdout

def test_conversion_file_path_cma_csv_success():
    filename = "S_NWC_CMA_MSG4_MSG-N-VISIR_20230313T093000Z"
    result = runner.invoke(app, ["convert", f"{RESOURCES_DIRECTORY + filename}.nc"])
    assert os.path.isfile(f"{OUTPUT_DIRECTORY + filename}.csv")
    assert result.exit_code == 0

def test_conversion_file_path_ct_csv_success():
    filename = "S_NWC_CT_MSG4_MSG-N-VISIR_20230313T094500Z"
    result = runner.invoke(app, ["convert", f"{RESOURCES_DIRECTORY + filename}.nc"])
    assert os.path.isfile(f"{OUTPUT_DIRECTORY + filename}.csv")
    assert result.exit_code == 0