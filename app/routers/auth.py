from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.login import Login

from app.services.auth_service import (
    login,
    register
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



# REGISTER USER

@router.post("/register")
def user_register(
    user: Login,
    role: str = "employee"
):

    return register(
        user.username,
        user.password,
        role
    )





# LOGIN USER (Swagger Authorize)

@router.post("/login")
def user_login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    token = login(
        form_data.username,
        form_data.password
    )


    if token is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    return token