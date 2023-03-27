import time
from watchdog.observers import Observer
from queue import Queue
from threading import Thread
from rich.progress import Progress, SpinnerColumn, TextColumn
from .filehandler import FileHandler
from .processor import Processor
from typing import Tuple


class Watcher:

    def __init__(self, input_path: str, output_path: str, export: str, recursive: bool, existing: bool,
                 lat_bounds: Tuple[int, int] | None, lon_bounds: Tuple[int, int] | None):
        self.observer = Observer()
        self.queue = Queue()
        self.file_handler = FileHandler(self.queue, input_path, recursive)
        self.processor = Processor(self.queue)
        self.input_path = input_path
        self.output_path = output_path
        self.export = export
        self.recursive = recursive
        self.existing = existing
        self.lat_bounds = lat_bounds
        self.lon_bounds = lon_bounds

    def run(self):

        # Set up a worker thread to process the queue of observed files
        worker = Thread(target=self.processor.process_load_queue, 
                        args=(self.output_path, self.export, self.lat_bounds, self.lon_bounds))
        worker.setDaemon(True)
        worker.start()

        # Retrieve pre-existing files 
        if self.existing:
            self.file_handler.load_existing_nc_files()

        self.observer.schedule(self.file_handler, self.input_path, self.recursive)
        self.observer.start()
        try:
            while True:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    progress.add_task(description="Watching and converting...", total=None)
                    time.sleep(5)
        finally:
            self.observer.stop()
            self.observer.join()
