#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: wikiserieswillemcli.py
#
# Copyright 2023 Willem Kuipers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for wikiserieswillemcli.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

import logging
import logging.config
import json
import argparse
import coloredlogs



from pathlib import Path
from pprint import pprint
from conf import ENCODING
from wikiserieswillemlib.wikiserieswillemlib import search_series
from wikiserieswillemcliexceptions import   SeriesFolderAlreadyExistsError, \
                                            SeriesNotFoundError, \
                                            InvalidNameError
                                        




__author__ = '''Willem Kuipers <willem@kuipers.co.uk>'''
__docformat__ = '''google'''
__date__ = '''01-05-2023'''
__copyright__ = '''Copyright 2023, Willem Kuipers'''
__credits__ = ["Willem Kuipers"]
__license__ = '''MIT'''
__maintainer__ = '''Willem Kuipers'''
__email__ = '''<willem@kuipers.co.uk>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''wikiserieswillemcli'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


def get_arguments():
    """
    Gets us the cli arguments.

    Returns the args as parsed from the argsparser.
    """
    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='''A template to create python libraries''')
    parser.add_argument('--log-config',
                        '-l',
                        action='store',
                        dest='logger_config',
                        help='The location of the logging config json file',
                        default='')
    parser.add_argument('--log-level',
                        '-L',
                        help='Provide the log level. Defaults to info.',
                        dest='log_level',
                        action='store',
                        default='info',
                        choices=['debug',
                                 'info',
                                 'warning',
                                 'error',
                                 'critical'])

    parser.add_argument('--name', '-n',
                        dest='name',
                        action='store',
                        help='Name of the Series you are trying to query',
                        type=str,
                        required=True)
    
    parser.add_argument('--output', '-o',
                        dest='output',
                        action='store',
                        help='Folder that you want to create the output in (defaults to local folder)',
                        type=str,
                        required=False)
    
    parser.add_argument('--force', '-F',
                        dest='force',
                        action='store_true',
                        help='Folder that you want to create the output in (defaults to local folder)',
                        default=False)

    parser.add_argument('--action','-a',
                        help='Action on what to do with the series.',
                        dest='action',
                        action='store',
                        default='add',
                        choices=['add',
                                 'remove'])

    args = parser.parse_args()
    return args


def is_valid_name(name: str):
    # Todo, implement other test cases
    if len(name) == 0:
        LOGGER.error("Name cannot be an empty string")
        return False
    return True


def setup_logging(level, config_file=None):
    """
    Sets up the logging.

    Needs the args to get the log level supplied

    Args:
        level: At which level do we log
        config_file: Configuration to use

    """
    # This will configure the logging, if the user has set a config file.
    # If there's no config file, logging will default to stdout.
    if config_file:
        # Get the config for the logger. Of course this needs exception
        # catching in case the file is not there and everything. Proper IO
        # handling is not shown here.
        try:
            with open(config_file) as conf_file:  # pylint: disable=unspecified-encoding
                configuration = json.loads(conf_file.read())
                # Configure the logger
                logging.config.dictConfig(configuration)
        except ValueError:
            print(f'File "{config_file}" is not valid json, cannot continue.')
            raise SystemExit(1)
    else:
        coloredlogs.install(level=level.upper())

def create_folder(path: Path):
    """
    Creates a folder idempotently.
    """
    if not path.exists():
        return path.mkdir(parents=True)
    LOGGER.debug(f'Folder {path} already exists')

def write_contents(path: Path, content: str, filemode="w", force=False):
    try:
        with open(path, filemode, encoding=ENCODING) as f:
            f.write(content)
    except FileExistsError:
        LOGGER.debug(f'File {path} already exists, force mode set to {force}')

def output_to_folders(name: str, series: dict, output_path, force=False):
    """
    Takes a series (name) with an output from the wikiserieswillemlib,
    converts it to a folder tree with metadata information.
    """
    cwd = Path.cwd() if output_path == None else Path(output_path)

    # Make sure the series folder is present
    series_folder = Path(cwd, name)
    create_folder(series_folder)

    # Add a marker that this folder is created by the CLI tool
    markerfile = Path(series_folder, '.wikiseries')
    write_contents(markerfile, "true")

    # loop over the series dict to parse all seasons and episodes
    for season, episodes in series.items():
        LOGGER.debug(f'Parsing season {season}')
        season_folder = Path(series_folder, season)
        create_folder(season_folder)

        for episode_number, episode_title in enumerate(episodes):
            file_path = Path(season_folder, f'Episode_{episode_number+1:02d}')
            filemode = "w" if  force else "x"
            file_content = f"Episode: {episode_number:02d}"

            write_contents(file_path, filemode=filemode, content=file_content, force=force)



def remove_folder(path: Path):
    # todo: check for hidden .wikiseries file, if that exists, remove the folder
    pass
        
def main():
    """
    Main method.

    This method holds what you want to execute when
    the script is run on command line.
    """
    args = get_arguments()
    setup_logging(args.log_level, args.logger_config)

    if args.action == "remove":
        # todo, implement
        pass

    # Check if the name is valid before making API calls
    name = args.name
    if not is_valid_name(name):
        raise InvalidNameError
    

    output_path = args.output
    if output_path == None:
        LOGGER.warning(f'Did not specify an output path, will save in local "{Path.cwd()}/{name}" folder.')


    try:
        series = search_series(args.name)
    except IndexError:
        # This should be fixed in the lib, not in the CLI
        LOGGER.error(f'Unable to parse series {name}. Not found on wikipedia?')
        raise SeriesNotFoundError
    

    output_to_folders(name, series, output_path, force=args.force)


if __name__ == '__main__':
    main()
