"""Exception handler."""
from fastapi import Request
from fastapi.responses import JSONResponse
from project.exceptions.project_exception import ProjectException
from project.utils.logger import logger


def register_exceptions_handler(app):
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exception: Exception):
        """Given an uncontrolled exception, logs it as an error and return a 500 HTTP Response"""
        logger.error(message=exception, code="UNCONTROLLED")
        return JSONResponse(
            status_code=500,
            content={"message": f"Failed to execute method {request.method}: {request.url}. {exception}"}
        )

    @app.exception_handler(ProjectException)
    async def exception_handler(request: Request, exception: ProjectException):
        """Given a validation exception, logs it as a warning and return a 422 HTTP Response"""
        logger.warning(message=exception.message, code=exception.code)
        return JSONResponse(
            status_code=422,
            content={"code": f"{exception.code}",
                     "message": f"Failed to execute method {request.method}: {request.url}. {exception.message}"}
        )
