# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Execute Orchestrator with Parameters """


from baseblock import FileIO

from micro_metrics.bp import Orchestrator


def run(input_directory: str,
        output_directory: str) -> str:
    metrics = Orchestrator().run(input_directory)
    FileIO.exists_or_create(output_directory)
    FileIO.write_json(metrics, output_directory)


def main(input_directory):
    run(input_directory)


if __name__ == "__main__":
    import plac

    plac.call(main)
