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
