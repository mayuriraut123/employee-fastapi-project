from fastapi import APIRouter, Depends


from app.core.security import verify_token
from app.core.roles import admin_required


from app.schemas.employee import Employee
from fastapi import BackgroundTasks

from app.services.background_service import generate_report


from app.services.employee_service import (
    insert_employee,
    get_all_employees,
    get_employee,
    update_employee,
    delete_employee
)



router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)




# VIEW - ADMIN + EMPLOYEE

@router.get("/")
def read_employees(
    user=Depends(verify_token)
):

    return get_all_employees()




# ADD - ADMIN ONLY

@router.post("/")
def add_employee(
    employee:Employee,
    user=Depends(admin_required)
):

    return insert_employee(
        employee.model_dump()
    )





# GET ONE - BOTH

@router.get("/{employee_id}")
def read_employee(
    employee_id:str,
    user=Depends(verify_token)
):

    return get_employee(
        employee_id
    )





# UPDATE - ADMIN ONLY

@router.put("/{employee_id}")
def update_employee_data(
    employee_id:str,
    employee:Employee,
    user=Depends(admin_required)
):

    return update_employee(
        employee_id,
        employee.model_dump()
    )





# DELETE - ADMIN ONLY

@router.delete("/{employee_id}")
def remove_employee(
    employee_id:str,
    user=Depends(admin_required)
):

    return delete_employee(
        employee_id
    )

@router.post("/report")
def create_report(
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        generate_report
    )

    return {
        "message": "Report generation started in background"
    }