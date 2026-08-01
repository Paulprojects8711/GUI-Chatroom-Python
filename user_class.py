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

class user:
    # username: string
    # address: tuple
    # lastSeen: int
    # lastSent: string
    # inVC: bool
    # mute: bool
    # deaf: bool
    def __init__(self, username, address, lastSeen, lastSent, inVC, mute, deaf):
        self.name = username
        self.address = address
        self.lastSeen = lastSeen
        self.lastSent = lastSent
        self.inVC = inVC
        self.mute = mute
        self.deaf = deaf
