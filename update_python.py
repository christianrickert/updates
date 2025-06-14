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
Summary:    Update Python modules via `pip` (2025-06-13)
URL:        https://github.com/christianrickert/updates
"""

# imports
import json
import os
import re
import subprocess
import sys


os.environ["PIP_DISABLE_PIP_VERSION_CHECK"] = "True"  # don't check PyPI for new version
os.environ["PIP_EXCLUDE"] = "packaging pip wheel"  # may be externally managed
missing_pattern = re.compile(r"^\S+ [^\s]+ requires (\S+), which is not installed\.$")
version_pattern = re.compile(
    r"^(\S+) [^\s]+ requires .+ but you have .+ incompatible\.$"
)


# functions
def check_current_modules():
    """Check current modules and install dependencies if necessary.

    Keyword arguments:
    None
    """
    print("=> Checking current modules...")
    check_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "check",
        ],
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    if check_result.stdout != "No broken requirements found.\n":
        missing_modules = set()
        for line in check_result.stdout.splitlines():
            missing_match = missing_pattern.match(line.strip())
            if missing_match:
                missing_modules.add(missing_match.group(1))
        if missing_modules:
            print("=> Installing missing modules...")
            print(f"ADD: {missing_modules}")
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--compile",
                    *missing_modules,
                ]
            )
    else:
        print("ADD: None")


def clear_module_cache():
    """Clear `pip` module cache.

    Keyword arguments:
    None
    """
    print("=> Clearing cached modules...")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "cache",
            "purge",
        ]
    )


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
            ]
        ).decode("utf-8")
    )  # name, version, latest_version, latest_filetype (keys)
    outdated_modules = [
        outdated_module["name"] for outdated_module in outdated_dictionary
    ] or None  # name (value)
    print(f"OLD: {outdated_modules}")
    return outdated_modules


def update_outdated_modules(outdated_modules=None):
    """Update outdated modules based on names from a `pip` JSON data structure.

    Keyword arguments:
    outdated_modules - list of outdated module names
    """
    print("=> Updating outdated modules...")
    if outdated_modules:
        print(f"NEW: {outdated_modules}")
        # update outdated modules
        upgrade_result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--compile",
                "--upgrade",
                *outdated_modules,
            ],
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        # restore outdated dependencies
        if upgrade_result.stderr:
            conflict_modules = set()
            for line in upgrade_result.stderr.splitlines():
                conflict_match = version_pattern.match(line.strip())
                if conflict_match:
                    conflict_modules.add(conflict_match.group(1))
            if conflict_modules:
                print("=> Restoring outdated modules...")
                print(f"KEEP: {conflict_modules}")
                subprocess.check_call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "--force-reinstall",
                        "--compile",
                        *conflict_modules,
                    ]
                )
            else:
                print(upgrade_result.stderr)
    else:
        print("NEW: None")


# main code
if __name__ == "__main__":
    print(f"=> Using Python executable:\n{sys.executable}")
    names = find_outdated_modules()
    update_outdated_modules(names)
    check_current_modules()
    clear_module_cache()
