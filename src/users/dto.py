from dataclasses import dataclass
from datetime import date


@dataclass
class UserCreateDTO:
    username: str
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    birthdate: date | None = None


@dataclass
class UserUpdateDTO:
    first_name: str | None = None
    last_name: str | None = None
    birthdate: date | None = None
    email: str | None = None


@dataclass
class UserPasswordChangeDTO:
    current_password: str
    new_password: str
