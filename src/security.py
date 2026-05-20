import base64
import os

from Crypto.Cipher import AES


def _pad(value: str) -> str:
    pad_length = AES.block_size - len(value.encode("utf-8")) % AES.block_size
    return value + chr(pad_length) * pad_length


def encryption_key() -> bytes:
    raw = os.getenv("TRAVEL_VISTA_AES_KEY", "dev-only-16-byte")
    return raw.encode("utf-8")[:16].ljust(16, b"0")


def encrypt_text(plain_text: str) -> str:
    cipher = AES.new(encryption_key(), AES.MODE_ECB)
    encrypted = cipher.encrypt(_pad(plain_text).encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

