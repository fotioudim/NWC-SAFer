from pathlib import Path
from queue import Queue
import xarray as xr
import pandas as pd
import time
import os
from rich import print
from .product import Product


class Processor:

    def __init__(self, *args):
        if len(args) > 0 and isinstance(args[0], Queue):
            self.queue = args[0]

    def process_load_queue(self, output_path: str, export: str):
        while True:
            if not self.queue.empty():
                event = self.queue.get()
                filename = event.src_path
                self.convert(filename, output_path, export)
            else:
                time.sleep(3)

    def convert(self, filename: str, output_path: str, export: str):
        print(":construction: [bright_yellow]Started[/bright_yellow] data processing for file:", filename)

        ds = xr.open_dataset(filename, chunks={'time': 10})
        product = ds.attrs['title']
        Path(output_path).mkdir(parents=True, exist_ok=True)
        output_filename = os.path.join(output_path, f"{Path(filename).stem}.{export}")
        final_df = pd.DataFrame()
        if product == Product.CT:
            ct = ds['ct'].to_dataframe()
            ctm = ds['ct_multilayer'].to_dataframe()
            final_df = pd.merge(ct, ctm, on=['ny', 'nx'])
        elif product == Product.CMA:
            cma_cs = ds['cma_cloudsnow'].to_dataframe()
            cma_v = ds['cma_volcanic'].to_dataframe()
            cma_d = ds['cma_dust'].to_dataframe()
            first_merge = pd.merge(cma_cs, cma_v, on=['ny', 'nx'])
            final_df = pd.merge(first_merge, cma_d, on=['ny', 'nx'])
        else:
            print(f":x: [red]Failed[/red] data conversion. Product type '{product}' is not supported yet.")

        if (export == "csv"):
            final_df.to_csv(output_filename)
        elif (export == "txt"):
            final_df.to_string(output_filename)
        elif (export == "excel"):
            final_df.to_excel(output_filename)
        print(":heavy_check_mark: [green]Completed[/green] data conversion for file:", output_filename)
