from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from prisma.errors import PrismaError

from domain.shared.exceptions import DomainNotFoundError, DomainConflictError, DomainBadRequestError 

def add_error_handlers(app_api: FastAPI):
  
  @app_api.exception_handler(DomainNotFoundError)
  async def handle_not_found_error(request: Request, exc: DomainNotFoundError):
    return JSONResponse(
      status_code=404,
      content={
        "error": "Not Found",
        "detail": str(exc)
      }
    )

  @app_api.exception_handler(DomainConflictError)
  async def handle_conflict_error(request: Request, exc: DomainConflictError):
    return JSONResponse(
      status_code=409,
      content={
        "error": "Conflict",
        "detail": str(exc)
      }
    )

  @app_api.exception_handler(DomainBadRequestError)
  async def handle_bad_request_error(request: Request, exc: DomainBadRequestError):
    return JSONResponse(
      status_code=400,
      content={
        "error": "Bad Request",
        "detail": str(exc)
      }
    )

  @app_api.exception_handler(PrismaError)
  async def handle_prisma_error(request: Request, exc: PrismaError):
    return JSONResponse(
      status_code=500,
      content={
        "error": "Database Error",
        "detail": "An unexpected database error occurred."
      }
    )

  @app_api.exception_handler(Exception)
  async def handle_generic_error(request: Request, exc: Exception):
    return JSONResponse(
      status_code=500,
      content={
        "error": "Internal Server Error",
        "detail": "An unexpected error occurred."
      }
    )
