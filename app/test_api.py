from dataclasses import asdict
from fastapi.applications import FastAPI
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from .common.error import http_422_error_handler, http_error_handler
from .common.custom_route import CustomRoute
from .routes.urls import router as api_router
from .database.database import database
from app.common.middleware.request_handle import RequestHandlingMiddleware
from app.common.middleware.sqlalchemy import SQLAlchemyMiddleware
import define
from app.utils.timestamp import timestamp


def create_app():
    PROJECT_NAME = f"Neubility-{define.SERVER_NAME.capitalize()}-Server"
    app = FastAPI(title=PROJECT_NAME)
    database.init_app(app)

    app.add_middleware(RequestHandlingMiddleware)
    app.add_middleware(SQLAlchemyMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)
    app.router.route_class = CustomRoute
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()


@app.get("/", include_in_schema=False)
async def index():
    print("aa")
    return Response(
        f"Test {define.SERVER_NAME.upper()} ( {timestamp.get_current_time()} )"
    )