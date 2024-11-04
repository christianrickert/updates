#!/usr/bin/env python3

"""
Copyright 2024 Christian Rickert

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Author:     Christian Rickert <rc.email@icloud.com>

Title:      update_python.py
Summary:    Update Python modules via `pip` (2024-11-04)
URL:        https://github.com/christianrickert/updates
"""

# imports
import json
import subprocess
import sys


# functions
def clear_module_cache():
    """Clear `pip` module cache.

    Keyword arguments:
    None
    """
    print("=> Clearing cached modules...")
    subprocess.check_call([sys.executable, "-m", "pip", "cache", "purge"])


def find_outdated_modules():
    """Get the list of outdated module names from a `pip` JSON data structure.

    Keyword arguments:
    None
    """
    print("=> Checking for outdated modules...")
    outdated_dictionary = json.loads(
        subprocess.check_output(
            [
                sys.executable,
                "-m",
                "pip",
                "list",
                "--outdated",
                "--format=json",
                "--disable-pip-version-check",
                "--exclude=pip",  # may be externally managed
            ]
        ).decode("utf-8")
    )  # name, version, latest_version, latest_filetype (keys)
    outdated_modules = [
        outdated_module["name"] for outdated_module in outdated_dictionary
    ] or None  # name (value)
    print(f"Old: {outdated_modules}")
    return outdated_modules


def update_outdated_modules(outdated_modules=None):
    """Update outdated modules based on names from a `pip` JSON data structure.

    Keyword arguments:
    outdated_modules - list of outdated module names
    """
    print("=> Updating outdated modules...")
    if outdated_modules:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade"]
            + [f"{outdated_module}" for outdated_module in outdated_modules]
        )
    else:
        print("New: None")


# main code
if __name__ == "__main__":
    print(f"=> Using Python executable:\n{sys.executable}")
    clear_module_cache()
    names = find_outdated_modules()
    update_outdated_modules(names)
