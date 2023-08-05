"""
Exceptions for the PylyBridge library.
"""


class APIError(Exception):
    """
    The exception that is raised when an API call fails.
    """

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


class UnexpectedNameError(Exception):
    """
    The exception that is raised when the slot deserializer encounters a name it doesn't expect.
    """
    def __init__(self, name, expected):
        super().__init__(f"Unexpected name: {name} (expected {expected})")


class UnexpectedTypeError(Exception):
    """
    The exception that is raised when the slot deserializer encounters a type it doesn't expect.
    """
    def __init__(self, type_, expected):
        super().__init__(f"Unexpected type: {type_} (expected {expected})")


class WrongNodeError(Exception):
    """
    The exception that is raised when the slot deserializer encounters a node ID it doesn't expect.
    """
    def __init__(self, node_id, expected):
        super().__init__(f"Unexpected node ID: {node_id} (expected {expected})")
