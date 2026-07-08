from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

import jwt


class PasswordHasher:
    """PBKDF2-HMAC-SHA256 password hashing (no native build dependencies)."""

    _iterations = 120_000

    def hash_password(self, password: str) -> str:
        salt = secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), self._iterations
        )
        return f"{salt}${digest.hex()}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        try:
            salt, expected = password_hash.split("$", maxsplit=1)
        except ValueError:
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), self._iterations
        )
        return hmac.compare_digest(digest.hex(), expected)


class JwtTokenService:
    def __init__(self, secret: str, algorithm: str, access_minutes: int) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._access_minutes = access_minutes

    def create_access_token(self, subject: str, role: str) -> str:
        expires_at = datetime.now(UTC) + timedelta(minutes=self._access_minutes)
        payload = {"sub": subject, "role": role, "type": "access", "exp": expires_at}
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(token, self._secret, algorithms=[self._algorithm])
