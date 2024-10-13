from sqlalchemy import Column, String, Integer
from sqlalchemy.types import JSON
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_app.db import Base
from auth_app.exceptions import InvalidPassword


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    password = Column(String)
    claims = Column(JSON)

    
async def get_user(session: AsyncSession, requested_user) -> User:
    result = await session.scalars(select(User).where(User.name==requested_user.name))
    user = result.first()
    if requested_user.password != user.password:
        raise InvalidPassword
    return user