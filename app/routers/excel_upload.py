from fastapi import APIRouter, UploadFile, File, Depends

from app.core.security import verify_token

from app.services.excel_service import save_excel



router = APIRouter(

    prefix="/excel",

    tags=["Excel Upload"]

)



@router.post("/upload")
def upload_excel(

    file: UploadFile = File(...),

    user = Depends(verify_token)

):

    return save_excel(file)