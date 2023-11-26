import logging
import uvicorn
import subprocess
from config import UVCRN_HOST, UVCRN_PORT, SSL_KEYFILE, SSL_SERTIF

from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastadmin import fastapi_app as admin_app

from auth.auth import auth_backend
from auth.models import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate, UserUpdate
from parse_news.router import get_router, schedule_parser_router, fill_ml
from auth.router import router as auth_check_router
from starlette.middleware.cors import CORSMiddleware
# from scrapyd_api import ScrapydAPI


def create_app() -> FastAPI:
    app = FastAPI(title="This is ХОРОШО!")

    origins = [
        "http://localhost:5173",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://194.54.176.118:*",
        "http://127.0.0.1:3000",
        "http://localhost:6800",
        "http://0.0.0.0:8005",
        "http://0.0.0.0:6800"
    ]

    init_logger('app')
    init_routers(app)
    init_middleware(app, origins)
    # init_scrapyd_sever()
    return app


def init_scrapyd_sever():
    subprocess.run(["scrapyd"],
                   stdout=subprocess.PIPE,
                   cwd="/home/alexander/PycharmProjects/Megahackathon_T17/src/parse_news/parse_news")


def init_routers(app: FastAPI) -> None:
    app.mount("/admin", admin_app)

    fastapi_users = FastAPIUsers[User, int](get_user_manager,
                                            [auth_backend]
                                            )

    app.include_router(fastapi_users.get_auth_router(auth_backend),
                       prefix="/auth/jwt",
                       tags=["auth"],
                       )
    app.include_router(fastapi_users.get_register_router(UserRead, UserCreate),
                       prefix="/auth",
                       tags=["auth"]
                       )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )

    app.include_router(get_router)
    app.include_router(auth_check_router)
    app.include_router(schedule_parser_router)
    app.include_router(fill_ml)


def init_middleware(app: FastAPI, origins_host: list):
    app.add_middleware(CORSMiddleware,
                       allow_origins=origins_host,
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"])


# Logging
def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = "%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s"
    logger.setLevel(logging.INFO)

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.ERROR)
    sh.addFilter(logger_filter)

    fh = logging.FileHandler(filename='app.log')
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.INFO)
    fh.addFilter(logger_filter)

    logger.addHandler(sh)
    logger.addHandler(fh)


def logger_filter(log: logging.LogRecord) -> int:
    if "password" in str(log.msg):
        return 0
    return 1


if __name__ == "__main__":
    uvicorn.run("main:create_app",
                host=UVCRN_HOST,
                port=int(UVCRN_PORT),
                ssl_keyfile=SSL_KEYFILE,
                ssl_certfile=SSL_SERTIF,
                factory=True,
                reload=True)
