from datetime import datetime, timedelta, timezone
from uuid import UUID

import bcrypt
import jwt

from src.config import settings
from src.common.constants import PASSWORD_MIN_LENGTH


class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def validate_password_strength(password: str) -> list[str]:
        errors = []

        if len(password) < PASSWORD_MIN_LENGTH:
            errors.append(
                f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"
            )

        if not any(char.isupper() for char in password):
            errors.append("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in password):
            errors.append("Password must contain at least one lowercase letter")

        if not any(char.isdigit() for char in password):
            errors.append("Password must contain at least one digit")

        return errors


class TokenManager:
    @staticmethod
    def create_access_token(user_id: UUID) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.security.access_token_expire_minutes
        )
        payload = {
            "sub": str(user_id),
            "exp": expire,
        }
        return jwt.encode(
            payload, settings.security.secret_key, algorithm=settings.security.algorithm
        )

    @staticmethod
    def verify_token(token: str) -> UUID | None:
        try:
            payload = jwt.decode(
                token,
                settings.security.secret_key,
                algorithms=[settings.security.algorithm],
            )
            user_id_str = payload.get("sub")
            return UUID(user_id_str) if user_id_str else None
        except (jwt.InvalidTokenError, ValueError, TypeError):
            return None
