import unittest
from queue import Queue
from pathlib import Path
from nwc_safer.filehandler import FileHandler

class TestFileHandler(unittest.TestCase):
    
    def test_load_existing_files_recursively(self):
        filehandler = FileHandler(Queue(), Path(".").resolve(), True)
        filehandler.load_existing_nc_files()
        self.assertFalse(filehandler.queue.empty())

    def test_load_existing_files_not_recursively(self):
        filehandler = FileHandler(Queue(), Path(".").resolve(), False)
        filehandler.load_existing_nc_files()
        self.assertTrue(filehandler.queue.empty())