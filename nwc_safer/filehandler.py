from watchdog.events import PatternMatchingEventHandler
from watchdog.events import FileCreatedEvent
from queue import Queue
import os
from rich import print


class FileHandler(PatternMatchingEventHandler):

    def __init__(self, queue: Queue, input_path: str, recursive: bool):
        PatternMatchingEventHandler.__init__(self, patterns=['*.nc'], ignore_directories=True, case_sensitive=False)
        self.queue = queue
        self.input_path = input_path
        self.recursive = recursive

    def on_created(self, event):
        print(":new: [blue]Found[/blue] a new file:", event.src_path)
        self.queue.put(event)

    def load_existing_nc_files(self):
        if (self.recursive):
            for root, dirs, files in os.walk(self.input_path):
                self.search_nc_in_file_list(root, files)
        else:
            self.search_nc_in_file_list(self.input_path, os.listdir(self.input_path))

    def search_nc_in_file_list(self, input_path: str, files: list[str]):
        for file in files:
            filename = os.path.join(input_path, file)
            if filename.endswith(".nc"):
                event = FileCreatedEvent(filename)
                print(":open_file_folder: [blue]Found[/blue] an existing file:", event.src_path)
                self.queue.put(event)
