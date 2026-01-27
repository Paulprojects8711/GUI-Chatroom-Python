from Crypto.Cipher import AES, ChaCha20_Poly1305
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
import base64

def derive_key(KEY: str, SALT: str) -> bytes:
    return PBKDF2(
        password=KEY.encode('utf-8'),
        salt=SALT.encode('utf-8'),
        dkLen=32,
        count=65536,
        hmac_hash_module=SHA256
    )

def decrypt(b64cipher: str, SALT: str, KEY: str) -> str:
    key = derive_key(KEY, SALT)

    iv = bytes(16)  # same as Java: new byte[16] for all zero IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    encrypted = base64.b64decode(b64cipher)
    decrypted = cipher.decrypt(encrypted)

    # remove PKCS5 padding
    pad_len = decrypted[-1]
    decrypted = decrypted[:-pad_len]

    return decrypted.decode('utf-8')

def encrypt(plaintext: str, SALT: str, KEY: str) -> str:
    key = derive_key(KEY, SALT)

    iv = bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    data = plaintext.encode('utf-8')

    # PKCS5 padding
    pad_len = 16 - (len(data) % 16)
    data += bytes([pad_len]) * pad_len

    encrypted = cipher.encrypt(data)

    return base64.b64encode(encrypted).decode()

def derive_key_bytes(KEY: str, SALT: str) -> bytes:
    key_bytes = bytearray(32)
    input_bytes = (KEY + SALT).encode('utf-8')
    for i in range(32):
        key_bytes[i] = input_bytes[i % len(input_bytes)]
    return bytes(key_bytes)

def encrypt_bytes(plaintext: bytes, SALT: str, KEY: str) -> bytes:
    key = derive_key(KEY, SALT)

    cipher = ChaCha20_Poly1305.new(key=key)

    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    # Java layout = nonce || ciphertext (which already includes tag at end)
    return cipher.nonce + ciphertext + tag

def decrypt_bytes(data: bytes, SALT: str, KEY: str) -> bytes:
    key = derive_key(KEY, SALT)

    nonce = data[:12]
    ciphertext = data[12:-16]
    tag = data[-16:]

    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)

    return cipher.decrypt_and_verify(ciphertext, tag)
