"""
    GUI-Chatroom-Python  An end-to-end encrypted Graphical User Interface Chatroom but remade in Python
    Copyright (C) 2026  Paul8711

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
"""

import json
import os
from pathlib import Path
from urllib import request, error

class DefaultKeyManager:
    GITHUB_URL = "https://raw.githubusercontent.com/paul8711-code/GUI-Chatroom/default-key/default_key.json"
    CACHE_FILE = Path.home() / ".gui-chatroom" / "default_key.json"

    def get_default_key():
        try:
            # cache directory exists
            DefaultKeyManager.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

            # download from GitHub
            try:
                with request.urlopen(DefaultKeyManager.GITHUB_URL, timeout=5) as response:
                    if response.status == 200:
                        content = response.read().decode("utf-8")
                        DefaultKeyManager.CACHE_FILE.write_text(content, encoding="utf-8")
            except error.URLError:
                print("Could not download default key from GitHub, using cached version if available.")

            # load from cache
            if DefaultKeyManager.CACHE_FILE.exists():
                json_content = DefaultKeyManager.CACHE_FILE.read_text(encoding="utf-8")
                return json.loads(json_content)
            else:
                print("No cached default key found.")
        except Exception as e:
            print("Error:", e)

        return None


# Testing
if __name__ == "__main__":
    key_data = DefaultKeyManager.get_default_key()
    if key_data:
        print("Default Key Version:", key_data.get("version"))
        print("Default Key:", key_data.get("key"))

