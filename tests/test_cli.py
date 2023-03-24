import unittest
from typer.testing import CliRunner
from nwc_safer.cli import app

runner = CliRunner()

class TestCli(unittest.TestCase):
    
    def test_app(self):
        result = runner.invoke(app)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("NWC-SAFer CLI tool --> NWC-SAF NetCDF data exporting and conversion made simple!" in result.stdout)

    def test_version(self):
        result = runner.invoke(app, ["--version"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("0.1.0" in result.stdout)

    def test_compatibility(self):
        result = runner.invoke(app, ["compatibility"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("NWC GEO Cloud Type Product" in result.stdout)
        self.assertTrue("NWC GEO Cloud Mask Product" in result.stdout)

    def test_conversion_no_file_path(self):
        result = runner.invoke(app, ["convert"])
        self.assertEqual(result.exit_code, 1)
        self.assertTrue("Missing value for '[FILE_PATHS]...'!" in result.stdout)

    def test_conversion_file_path_not_exists(self):
        result = runner.invoke(app, ["convert", "test.nc"])
        self.assertEqual(result.exit_code, 1)
        self.assertTrue("Invalid value for '[FILE_PATHS]...': File 'sda' does not exist." in result.stdout)

    def test_conversion_file_path_not_exists(self):
        result = runner.invoke(app, ["convert", "."])
        self.assertEqual(result.exit_code, 2)
        self.assertTrue("Invalid value for '[FILE_PATHS]...': File '.' is a directory." in result.stdout)

    
