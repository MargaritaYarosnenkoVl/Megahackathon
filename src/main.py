from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastadmin import fastapi_app as admin_app

from src.auth.auth import auth_backend
from src.auth.models import User
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.parse_news.router import router as router_parser
from src.parse_news.router import launch_parser as launch_parser_router
from src.auth.router import router as auth_check_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="This is ХОРОШО!"
)

origins = [
    "http://localhost:5173",
    "localhost:5173",
    "localhost:3000",
    "194.54.176.118:*"
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

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


app.include_router(router_parser)
app.include_router(auth_check_router)
app.include_router(launch_parser_router)