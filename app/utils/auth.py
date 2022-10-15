from passlib.context import CryptContext
from jose import jwt

# 나중에 os로 뺴야함 #os.environ["JWT_SECRET_KEY"]
# os.environ["JWT_REFRESH_SECRET_KEY"]


class AuthManager:
    def __init__(self):
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 day
        self.ALGORITHM = "HS256"
        self.JWT_SECRET_KEY = (
            "test_jwt_key_value"
        )
        self.JWT_REFRESH_SECRET_KEY = "test_jwt_refresh_key_value" 
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def decode_jwt(self, token: str):
        return jwt.decode(
            token, self.JWT_REFRESH_SECRET_KEY, algorithms=[self.ALGORITHM]
        )


auth_manager = AuthManager()