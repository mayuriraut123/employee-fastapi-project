from fastapi import APIRouter, UploadFile, File, Depends

from app.core.security import verify_token

from app.services.csv_service import save_csv



router = APIRouter(
    prefix="/csv",
    tags=["CSV Upload"]
)



@router.post("/upload")
def upload_csv(

    file: UploadFile = File(...),

    user = Depends(verify_token)

):

    return save_csv(file)