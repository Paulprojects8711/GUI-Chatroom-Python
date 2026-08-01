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

import os
import base64
import hashlib
import hmac

ITERATIONS = 65536
KEY_LENGTH = 32  # 256 bits = 32 bytes
SALT_LENGTH = 16


def hash(inp: str) -> str:
    salt = os.urandom(SALT_LENGTH)
    hash_bytes = hashlib.pbkdf2_hmac(
        'sha256',
        inp.encode('utf-8'),
        salt,
        ITERATIONS,
        dklen=KEY_LENGTH
    )
    return f"{base64.b64encode(salt).decode()}:{base64.b64encode(hash_bytes).decode()}"


def verify(inp: str, stored: str) -> bool:
    salt_b64, hash_b64 = stored.split(":")
    salt = base64.b64decode(salt_b64)
    stored_hash = base64.b64decode(hash_b64)

    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        inp.encode('utf-8'),
        salt,
        ITERATIONS,
        dklen=KEY_LENGTH
    )

    # Constant-time comparison (equivalent to your XOR loop)
    return hmac.compare_digest(new_hash, stored_hash)
