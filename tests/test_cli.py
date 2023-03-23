import unittest
from typer.testing import CliRunner
from nwc_safer.cli import app

runner = CliRunner()

class TestCli(unittest.TestCase):
    
    def test_app(self):
        result = runner.invoke(app)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("NWC-SAF NetCDF Data Exporter || CLI tool" in result.stdout)

    def test_compatibility(self):
        result = runner.invoke(app, ["compatibility"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("NWC GEO Cloud Type Product" in result.stdout)
        self.assertTrue("NWC GEO Cloud Mask Product" in result.stdout)

    
