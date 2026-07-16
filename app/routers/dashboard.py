from fastapi import APIRouter, Depends

from app.core.security import verify_token

from app.services.dashboard_service import (
    total_employee,
    department_count,
    average_salary,
    highest_salary
)



router = APIRouter(

    prefix="/dashboard",

    tags=["Dashboard"]

)



@router.get("/total")
def get_total(
    user=Depends(verify_token)
):

    return total_employee()




@router.get("/department")
def get_department(
    user=Depends(verify_token)
):

    return department_count()




@router.get("/average-salary")
def get_average_salary(
    user=Depends(verify_token)
):

    return average_salary()




@router.get("/highest-salary")
def get_highest_salary(
    user=Depends(verify_token)
):

    return highest_salary()