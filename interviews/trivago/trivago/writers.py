"""
Place where stuff which knows how to export data lives.
"""

import abc

import json

import yaml


class BaseWriter(metaclass=abc.ABCMeta):
    """
    Write data rows to dest.

    Supposed to be used as context manager.
    """

    @abc.abstractmethod
    def __call__(self, row):
        """
        Process one row: write to file, save to buffer or whatever.
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Put your finalization work here: flush buffers, close files, etc.
        """
        pass


class BaseFileWriter(BaseWriter, metaclass=abc.ABCMeta):
    def __init__(self, file_name):
        self.file_name = file_name

    def __enter__(self):
        self.file = open(self.file_name, "w")
        return super(BaseFileWriter, self).__enter__()

    def __exit__(self, *args, **kwargs):
        self.file.close()
        super(BaseFileWriter, self).__exit__(*args, **kwargs)


class JsonWriter(BaseFileWriter):
    def __call__(self, row):
        json.dump(row, self.file, sort_keys=True)
        self.file.write(json.dumps(row, sort_keys=True))
        self.file.write("\n")


class YAMLWriter(BaseFileWriter):
    def __call__(self, row):
        yaml.safe_dump((dict(row), ), self.file, default_flow_style=False)
