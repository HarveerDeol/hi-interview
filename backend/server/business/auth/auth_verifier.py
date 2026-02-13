from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import jwt

from server.business.auth.schema import UserTokenInfo
from server.shared.config import Config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthVerifier:
    def __init__(self, config: Config):
        self.config = config

    def get_user_token_info(
        self, token: str = Depends(oauth2_scheme)
    ) -> UserTokenInfo:
        try:
            payload = jwt.decode(
                token, self.config.access_token_secret_key, algorithms=["HS256"]
            )
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )
            return UserTokenInfo(user_id=user_id)
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    def UserTokenInfo(self) -> UserTokenInfo:
        return Depends(self.get_user_token_info)
