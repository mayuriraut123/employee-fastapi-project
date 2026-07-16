from fastapi import Depends,HTTPException

from app.core.security import verify_token



def admin_required(
    user=Depends(verify_token)
):


    if user.get("role") != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


    return user