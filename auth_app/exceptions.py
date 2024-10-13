from fastapi import HTTPException

class InvalidPassword(HTTPException):
    status_code=400
    detail="не верное имя пользователя или пароль"


