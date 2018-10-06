#!/bin/python

import argparse

def get_argument_parser():
    """

    :return:
    """
    parser = argparse.ArgumentParser(
        prog='license-adder',
        description='Adds license files to repositories in the given GitHub project.'
    )
    parser.add_argument(
        '-h',
        '--help',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '-p',
        '--project',
        action='store',
        dest='project',
    )

    return parser

def main():
    parser = get_argument_parser()
    args = parser.parse_args()

    project_name = args.project

if __name__  == "__main__":
    main()
