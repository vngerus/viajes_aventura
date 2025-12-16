import hashlib
import os

_ITERATIONS = 100_000


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        _ITERATIONS
    )
    return salt.hex() + pwd_hash.hex()


def verify_password(stored_hash: str, password: str) -> bool:
    salt = bytes.fromhex(stored_hash[:32])
    saved_hash = stored_hash[32:]

    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        _ITERATIONS
    )
    return pwd_hash.hex() == saved_hash
