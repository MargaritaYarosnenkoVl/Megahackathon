from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend, BearerTransport
from src.config import SECRET
cookie_transport = CookieTransport(cookie_name="news",
                                   cookie_max_age=3600,
                                   cookie_secure=False,
                                   cookie_httponly=False)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# SECRET = os.getenv("SECRET")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET,
                       lifetime_seconds=3600,
                       token_audience=["*"])


auth_backend = AuthenticationBackend(name="jwt",
                                     transport=bearer_transport,
                                     get_strategy=get_jwt_strategy
                                     )
