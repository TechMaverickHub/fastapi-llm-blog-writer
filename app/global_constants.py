from enum import Enum


class SuccessMessage(str, Enum):
    """Success messages used across the application."""

    RECORD_CREATED = "Record created successfully."
    RECORD_UPDATED = "Record updated successfully."
    RECORD_DELETED = "Record deleted successfully."
    RECORD_RETRIEVED = "Record retrieved successfully."

    LOGIN_SUCCESS = "Login successful."


class ErrorMessage(str, Enum):
    """Error messages used across the application."""

    BAD_REQUEST = "Bad request."
    NOT_FOUND = "Record not found."
    SOMETHING_WENT_WRONG = "Something went wrong. Please try again later."

class ErrorKeys(str, Enum):
    NON_FIELD_ERROR = "detail"