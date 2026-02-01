from uuid import UUID


class UserError(Exception):
    http_status_code = 500

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class UserNotFoundError(UserError):
    http_status_code = 404

    def __init__(self, identifier: str | UUID):
        self.identifier = identifier
        message = f"User with identifier {identifier} not found"
        details = {"identifier": str(identifier)}
        super().__init__(message, details)


class UserAlreadyExistsError(UserError):
    http_status_code = 400

    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        message = f"User with {field} '{value}' already exists"
        details = {"field": field, "value": value}
        super().__init__(message, details)


class InvalidPasswordError(UserError):
    http_status_code = 400

    def __init__(self, errors: list[str]):
        self.errors = errors
        message = f"Password validation failed: {'; '.join(errors)}"
        details = {"errors": errors}
        super().__init__(message, details)


class InvalidCredentialsError(UserError):
    http_status_code = 401

    def __init__(self):
        message = "Invalid username or password"
        super().__init__(message)
