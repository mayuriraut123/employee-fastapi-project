from jose import jwt

from datetime import datetime,timedelta



SECRET_KEY="mysecretkey123"

ALGORITHM="HS256"




def create_access_token(data:dict):


    expire = datetime.utcnow() + timedelta(
        minutes=30
    )


    data.update(
        {
            "exp":expire
        }
    )


    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    return token