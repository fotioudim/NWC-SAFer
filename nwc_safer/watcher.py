import time
from watchdog.observers import Observer
from queue import Queue
from threading import Thread
from rich.progress import Progress, SpinnerColumn, TextColumn
from .filehandler import FileHandler
from .processor import Processor


class Watcher:

    def __init__(self, input_path: str, output_path: str, export: str, recursive: bool, existing: bool):
        self.observer = Observer()
        self.queue = Queue()
        self.file_handler = FileHandler(self.queue, input_path, recursive)
        self.processor = Processor(self.queue)
        self.input_path = input_path
        self.output_path = output_path
        self.export = export
        self.recursive = recursive
        self.existing = existing

    def run(self):

        # Set up a worker thread to process the queue of observed files
        worker = Thread(target=self.processor.process_load_queue, args=(self.output_path, self.export))
        worker.setDaemon(True)
        worker.start()

        # Retrieve pre-existing files 
        if (self.existing):
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
