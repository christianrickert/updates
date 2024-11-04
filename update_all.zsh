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

Title:      update_all.py
Summary:    Update Homebrew, Rust, and Python (2024-11-04)
URL:        https://github.com/christianrickert/updates
"""

clear
echo "================================================================================"
echo "                                      Brew                                      "
echo "================================================================================"
brew update && yes | brew upgrade --verbose && brew autoremove && brew cleanup --scrub
echo
echo "================================================================================"
echo "                                      Rust                                      "
echo "================================================================================"
rustup self update && rustup update
echo
echo "================================================================================"
echo "                                     Python                                     "
echo "================================================================================"
python ~/update_python.py
echo
