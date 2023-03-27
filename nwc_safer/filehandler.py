from watchdog.events import PatternMatchingEventHandler
from watchdog.events import FileCreatedEvent
from queue import Queue
import os
from rich import print


class FileHandler(PatternMatchingEventHandler):
    """
    FileHandler class is responsible for handling file events and
    pushing new or existing files to a queue, in order to be processed afterward
    """


    def __init__(self, queue: Queue, input_path: str, recursive: bool):
        """
        FileHandler constructor defines that the target are files with .nc extension
        """
        PatternMatchingEventHandler.__init__(self, patterns=['*.nc'], ignore_directories=True, case_sensitive=False)
        self.queue = queue
        self.input_path = input_path
        self.recursive = recursive


    def on_created(self, event):
        """
        Event triggered when a new NetCDF file is created/added 
        to the observed directories
        """
        print(":new: [blue]Found[/blue] a new file:", event.src_path)
        self.queue.put(event)


    def load_existing_nc_files(self):
        """
        Load existing NetCDF files in a directory. 
        There is the option to track files to its corresponding subdirectories
        """
        if self.recursive:
            for root, dirs, files in os.walk(self.input_path):
                self.search_nc_in_file_list(root, files)
        else:
            self.search_nc_in_file_list(self.input_path, os.listdir(self.input_path))


    def search_nc_in_file_list(self, input_path: str, files: list[str]):
        """
        Load existing NetCDF files from a single directory
        """
        for file in files:
            filename = os.path.join(input_path, file)
            if filename.endswith(".nc"):
                event = FileCreatedEvent(filename)
                print(":open_file_folder: [blue]Found[/blue] an existing file:", event.src_path)
                self.queue.put(event)
