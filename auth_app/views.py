from fastapi import Depends, APIRouter
from fastapi_utils.cbv import cbv

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from auth_app.db import get_session
from auth_app.models import User, get_user
from sqlalchemy.exc import IntegrityError
import jwt
SIGNATURE = "top_secrets"

router = APIRouter()


class UserSchema(BaseModel):
    name: str
    password: str
    claims: dict

class UserLoginSchema(BaseModel):
    name: str
    password: str

@cbv(router)
class LoginView:
    @router.post("/users/", tags=["users"], response_model=UserSchema)
    async def add_user(self, user: UserSchema, session: AsyncSession = Depends(get_session)):
        new_user = User(name=user.name, password=user.password, claims=user.claims)
        try:
            session.add(new_user)
            await session.commit()
            return new_user
        except IntegrityError as ex:
            await session.rollback()
            raise IntegrityError("Пользоватеть с таким именем уже существует")
        

    @router.post("/login/", tags=["login"])
    async def login(self, requested_user: UserLoginSchema, session: AsyncSession = Depends(get_session)):
        user = await get_user(session, requested_user)
        token_payload = {
            "claims": user.claims,
            "username": user.name
        }

        encoded_jwt = jwt.encode(token_payload, SIGNATURE)
        return {"token": encoded_jwt}