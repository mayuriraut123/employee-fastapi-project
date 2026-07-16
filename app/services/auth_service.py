from app.core.database import db
from app.core.auth import create_access_token

from passlib.context import CryptContext



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



users = db["users"]




# REGISTER

def register(
    username:str,
    password:str,
    role:str="employee"
):


    existing_user = users.find_one(
        {
            "username":username
        }
    )


    if existing_user:

        return {
            "message":"User already exists"
        }



    hashed_password = pwd_context.hash(
        password
    )



    users.insert_one(
        {
            "username":username,
            "password":hashed_password,
            "role":role
        }
    )



    return {
        "message":"User registered successfully"
    }





# LOGIN

def login(
    username:str,
    password:str
):


    user = users.find_one(
        {
            "username":username
        }
    )


    if not user:

        return None



    if not pwd_context.verify(
        password,
        user["password"]
    ):

        return None




    token = create_access_token(
        {
            "sub":username,
            "role":user.get(
                "role",
                "employee"
            )
        }
    )


    return {

        "access_token":token,

        "token_type":"bearer"

    }