from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def get_response_schema(schema: dict, message: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "message": message,
            "status": status_code,
            "results": jsonable_encoder(schema),
        },
    )