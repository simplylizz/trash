import csv
import contextlib


@contextlib.contextmanager
def csv_reader(file_name: str):
    with open(file_name, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        yield csv_reader
