#!/usr/bin/env python3

import argparse
import contextlib
import logging

import readers
import validators
import writers


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    return parser.parse_args()


def main():
    args = parse_args()

    with contextlib.ExitStack() as stack:
        reader = stack.enter_context(readers.csv_reader(args.input))
        writers_list = [stack.enter_context(w) for w in (
            writers.JsonWriter(args.input.split(".", 1)[0] + ".out.json"),
            writers.YAMLWriter(args.input.split(".", 1)[0] + ".out.yaml"),
        )]

        for line in reader:
            row = validators.hotel_validator(line)
            if row is not None:
                for writer in writers_list:
                    writer(row)


if __name__ == "__main__":
    main()
