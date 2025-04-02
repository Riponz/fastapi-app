from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from exception_handlers import BookBaseException


from routes import book_router

app = FastAPI()

app.include_router(book_router, prefix="/api/v1")

@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code":  exc.status_code,
            "message" : "failed",
            "error": exc.detail
        }
    )

@app.exception_handler(BookBaseException)
async def integrity_error_handler(request: Request, exc : BookBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message" : "failed",
            "error" : str(exc)
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "status_code" : 400,
            "messages" : "failed",
            "error": exc.errors()[0]['msg']
        }
        )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")