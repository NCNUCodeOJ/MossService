"""
define custom exception
"""
class CustomException(Exception):
    """
    custom exception base class
    """
    def __init__(self, message):
        super().__init__()
        self.message = message


class ClientError(CustomException):
    """
    exception of judge client error
    """
