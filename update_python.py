#!/usr/bin/env python3

# imports
import json
import subprocess
import sys


# functions
def find_outdated_modules():
    """Get the list of outdated module names from a `pip` JSON data structure.

    Keyword arguments:
    None
    """
    print("Checking for outdated modules...")
    outdated_dictionary = json.loads(
        subprocess.check_output(
            [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"]
        ).decode("utf-8")
    )  # name, version, latest_version, latest_filetype (keys)
    outdated_modules = [
        outdated_module["name"] for outdated_module in outdated_dictionary
    ] or None  # name (values)
    print(f"\tOld: {outdated_modules}")
    return outdated_modules


def update_outdated_modules(outdated_modules=None):
    """Update outdated modules based on names from a `pip` JSON data structure.

    Keyword arguments:
    outdated_modules - list of outdated module names
    """
    print("Updating outdated modules...")
    if outdated_modules:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade"]
            + [f"{outdated_module}" for outdated_module in outdated_modules]
        )
    else:
        print("\tNew: None")


# main code
if __name__ == "__main__":
    names = find_outdated_modules()
    update_outdated_modules(names)
