#!/usr/bin/env python

import argparse
import yaml
import os
import datetime

banner = """
______               _           _
| ___ \             (_)         | |
| |_/ /___ _ __ ___  _ _ __   __| | ___ _ __
|    // _ \ '_ ` _ \| | '_ \ / _` |/ _ \ '__|
| |\ \  __/ | | | | | | | | | (_| |  __/ |
\_| \_\___|_| |_| |_|_|_| |_|\__,_|\___|_|
"""

config = {
    "max_to_keep": 64,
    "max_to_show": 4,
}

help_config = {
    "max_to_keep": "Maximum number of reminders to be kept in database.",
    "max_to_show": "Maximum number of reminders to be shown.",
}

database = []

path_basefolder = "$HOME/.reminder"


def show_banner():
    print(banner)


def show_config_help():
    print(
        "The config is written in the YAML format. The following keywords can be set:"
    )
    global config
    global help_config
    for key in config:
        print("{0:<16} : {1}".format(key, help_config[key]))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=
        "Tiny command-line app to remind yourself what your former self wanted to do."
    )

    parser.add_argument(
        "--help-config",
        action="store_true",
        default=False,
        help="Print help for syntax of the config file.")

    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose mode for debugging.")

    parser.add_argument(
        "-m", "--message", type=str, help="Add reminder message.")

    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        default=False,
        help="Delete last reminder message.")

    return parser.parse_args()


def add_message(text, verbose):
    global database
    timestamp = "{:%d-%b-%Y %H:%M:%S}".format(datetime.datetime.now())
    if verbose:
        print("Add message with text {} and timestamp {}.".format(
            text, timestamp))
    database = [{"text": text, "time": timestamp}] + database
    if len(database) > config["max_to_keep"]:
        if verbose:
            print(
                "Database has {} entries, reduce to newest {} entries.".format(
                    len(database), config["max_to_keep"]))
        database = database[0:config["max_to_keep"]]

    filename_database = "database.yaml"
    path_database = os.path.join(path_basefolder, filename_database)
    if verbose:
        print("Write database to {}.".format(path_database))
    yaml.dump(database, open(path_database, "w"), default_flow_style=False)


def delete_last_message(verbose):
    global database
    if len(database) != 0:
        if verbose:
            print("Remove message with text {} and timestamp {}.".format(
                database[0]["text"], database[0]["time"]))
        database = database[1:]
    filename_database = "database.yaml"
    path_database = os.path.join(path_basefolder, filename_database)
    if verbose:
        print("Write database to {}.".format(path_database))
    yaml.dump(database, open(path_database, "w"), default_flow_style=False)


def show_reminders(verbose):
    if verbose:
        print("Show first {} messages.".format(config["max_to_show"]))
    for m in reversed(database[:config["max_to_show"]]):
        print("{:<20} : {}".format(m["time"], m["text"]))


def load_config_and_database(verbose):
    global path_basefolder
    if verbose:
        print("Use basepath {} for config and dataset files.".format(
            path_basefolder))
    path_basefolder = os.path.expandvars(path_basefolder)
    if verbose:
        print("Expand basepath to {}.".format(path_basefolder))

    if not os.path.isdir(path_basefolder):
        os.mkdir(path_basefolder)

    global config
    filename_config = "config.yaml"
    path_config = os.path.join(path_basefolder, filename_config)
    if verbose:
        print("Load config from path {}.".format(path_config))
    if not os.path.isfile(path_config):
        yaml.dump(config, open(path_config, "w"), default_flow_style=False)

    config = yaml.load(open(path_config))
    if verbose:
        print("Loaded config {}.".format(config))

    global database
    filename_database = "database.yaml"
    path_database = os.path.join(path_basefolder, filename_database)
    if verbose:
        print("Load database from path {}.".format(path_database))
    if not os.path.isfile(path_database):
        yaml.dump(database, open(path_database, "w"), default_flow_style=False)

    database = yaml.load(open(path_database))
    if verbose:
        print("Loaded {} messages.".format(len(database)))


if __name__ == "__main__":
    args = parse_arguments()
    load_config_and_database(args.verbose)

    if args.help_config:
        show_config_help()
        os._exit(0)

    if args.delete:
        delete_last_message(args.verbose)
        os._exit(0)

    if args.message:
        add_message(args.message, args.verbose)

    show_banner()
    show_reminders(args.verbose)
