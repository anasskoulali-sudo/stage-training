"""Password hashing and verification for MySQL-stored credentials."""

import hmac

import bcrypt

_BCRYPT_HASH_LENGTH = 60


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, stored: str) -> bool:
    if not plain or not stored:
        return False
    stored = stored.strip()
    try:
        hashed = stored.encode("utf-8")
        if hashed.startswith(b"$2y$"):
            hashed = b"$2b$" + hashed[4:]
        if hashed.startswith((b"$2a$", b"$2b$", b"$2x$")):
            if len(stored) < _BCRYPT_HASH_LENGTH:
                return False
            return bcrypt.checkpw(plain.encode("utf-8"), hashed)
    except (ValueError, TypeError):
        return False
    # Seed rows were stored as plaintext because the column was too short for bcrypt.
    return hmac.compare_digest(plain.encode("utf-8"), stored.encode("utf-8"))


def verify_plain(plain: str, stored: str | None) -> bool:
    if not plain or not stored:
        return False
    stored = stored.strip()
    if not stored:
        return False
    return hmac.compare_digest(plain.encode("utf-8"), stored.encode("utf-8"))
