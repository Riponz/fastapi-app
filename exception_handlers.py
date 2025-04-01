from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

class BookBaseException(Exception):
    status_code = 500


class BookIntegrityException(BookBaseException):
    status_code = 400

    def __init__(self,message):
        super().__init__(message)

class BookOperationalException(BookBaseException):
    status_code = 500

    def __init__(self,message):
        super().__init__(message)

class BookDataException(BookBaseException):
    status_code = 422
    def __init__(self,message):
        super().__init__(message)

class BookTimeOutException(BookBaseException):
    status_code = 400

    def __init__(self,message):
        super().__init__(message)

