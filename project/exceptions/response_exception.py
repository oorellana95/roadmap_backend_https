"""Response Exception Classes"""
from project.exceptions.project_exception import ProjectException


class ResponseException(ProjectException):
    def __init__(self):
        super().__init__()
        self.code = "ERROR.RESPONSE"


class NotFoundException(ResponseException):
    def __init__(self, message):
        super().__init__()
        self.message = message
