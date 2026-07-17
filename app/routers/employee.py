from fastapi import APIRouter, Depends

from app.core.security import verify_token
from app.schemas.employee import Employee
from app.decorators.employee_decorator import employee_logger
from app.services.employee_service import (
    insert_employee,
    get_all_employees,
    get_employee,
    update_employee,
    delete_employee
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    dependencies=[Depends(verify_token)]
)


# POST
@router.post("/")
@employee_logger
def add_employee(employee: Employee):
    print("Request:", employee.model_dump())

    response = insert_employee(employee.model_dump())

    print("Response:", response)
    return response


# GET ALL
@router.get("/")
@employee_logger
def read_employees(
    page: int = 1,
    limit: int = 10,
    department: str = None
):
    print(f"Request -> page={page}, limit={limit}, department={department}")

    response = get_all_employees(page, limit, department)

    print("Response:", response)
    return response


# GET ONE
@router.get("/{employee_id}")
@employee_logger
def read_employee(employee_id: str):
    print(f"Request -> employee_id={employee_id}")

    response = get_employee(employee_id)

    print("Response:", response)
    return response


# UPDATE
@router.put("/{employee_id}")
@employee_logger
def update(employee_id: str, employee: Employee):
    print(f"Request -> employee_id={employee_id}")
    print("Updated Data:", employee.model_dump())

    response = update_employee(
        employee_id,
        employee.model_dump()
    )

    print("Response:", response)
    return response


# DELETE
@router.delete("/{employee_id}")
@employee_logger
def delete(employee_id: str):
    print(f"Request -> employee_id={employee_id}")

    response = delete_employee(employee_id)

    print("Response:", response)
    return response