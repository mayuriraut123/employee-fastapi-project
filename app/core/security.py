from fastapi import Depends,HTTPException

from fastapi.security import OAuth2PasswordBearer

from jose import jwt



SECRET_KEY="mysecretkey123"

ALGORITHM="HS256"



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)




def verify_token(
    token:str=Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                ALGORITHM
            ]
        )


        return payload



    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )