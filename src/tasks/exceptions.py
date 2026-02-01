from uuid import UUID


class TaskError(Exception):
    http_status_code = 500

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class TaskNotFoundError(TaskError):
    http_status_code = 404

    def __init__(self, task_id: UUID):
        self.task_id = task_id
        message = f"Task with ID {task_id} not found"
        details = {"task_id": str(task_id)}
        super().__init__(message, details)


class TaskValidationError(TaskError):
    http_status_code = 400

    def __init__(self, message: str, field: str | None = None):
        self.field = field
        details = {"field": field} if field else {}
        super().__init__(message, details)
