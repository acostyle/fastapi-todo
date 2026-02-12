from uuid import UUID

from src.security import PasswordHasher, TokenManager
from src.users.dto import UserCreateDTO, UserReadDTO
from src.users.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidPasswordError,
    InvalidCredentialsError,
)
from src.users.models import User
from src.users.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.password_hasher = PasswordHasher()

    @staticmethod
    def _normalize_username(username: str) -> str:
        return username.strip().lower()

    @staticmethod
    def _normalize_email(email: str) -> str:
        return email.strip().lower()

    async def create_user(self, user_data: UserCreateDTO) -> UserReadDTO:
        normalized_username = self._normalize_username(user_data.username)
        normalized_email = self._normalize_email(user_data.email)

        password_errors = self.password_hasher.validate_password_strength(
            user_data.password
        )
        if password_errors:
            raise InvalidPasswordError(password_errors)

        existing_user_by_username = await self.repository.get_by_username(
            normalized_username
        )
        if existing_user_by_username:
            raise UserAlreadyExistsError("username", normalized_username)

        existing_user_by_email = await self.repository.get_by_email(normalized_email)
        if existing_user_by_email:
            raise UserAlreadyExistsError("email", normalized_email)

        hashed_password = self.password_hasher.hash_password(user_data.password)

        user_dto = UserCreateDTO(
            username=normalized_username,
            email=normalized_email,
            password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            birthdate=user_data.birthdate,
        )

        created_user = await self.repository.create(user_dto)
        return self._to_user_read_dto(created_user)

    async def get_user(self, user_id: UUID) -> UserReadDTO:
        user = await self.repository.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        return self._to_user_read_dto(user)

    async def login(self, username: str, password: str) -> str:
        normalized_username = self._normalize_username(username)

        user = await self.repository.get_by_username(normalized_username)
        if not user:
            raise InvalidCredentialsError()

        hashed_password = user.hashed_password
        if not self.password_hasher.verify_password(password, hashed_password):
            raise InvalidCredentialsError()

        token = TokenManager.create_access_token(user.id)
        return token

    @staticmethod
    def _to_user_read_dto(user: User) -> UserReadDTO:
        return UserReadDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            birthdate=user.birthdate,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
