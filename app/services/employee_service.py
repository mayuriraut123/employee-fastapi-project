from bson import ObjectId

from app.core.database import employee_collection
from app.decorators.employee_decorator import employee_logger, exception_handler


# Insert Employee
@employee_logger
@exception_handler
def insert_employee(employee):

    print("Inside insert_employee()")

    result = employee_collection.insert_one(employee)

    print("Employee inserted successfully")

    return {

        "message": "Employee Added",

        "id": str(result.inserted_id)

    }


# Get All Employees
@employee_logger
@exception_handler
def get_all_employees(
        page=1,
        limit=10,
        department=None
):

    print("Inside get_all_employees()")

    employees = []

    skip = (page - 1) * limit

    query = {}

    if department:

        query["department"] = department

    total = employee_collection.count_documents(query)

    result = employee_collection.find(query)\
        .skip(skip)\
        .limit(limit)

    for employee in result:

        employee["_id"] = str(employee["_id"])

        employees.append(employee)

    print("Employees fetched successfully")

    return {

        "page": page,

        "limit": limit,

        "total": total,

        "data": employees

    }


# Get One Employee
@employee_logger
@exception_handler
def get_employee(employee_id):

    print("Inside get_employee()")

    employee = employee_collection.find_one(
        {
            "_id": ObjectId(employee_id)
        }
    )

    if employee:

        employee["_id"] = str(employee["_id"])

        print("Employee found")

        return employee

    print("Employee not found")

    return {

        "message": "Employee Not Found"

    }


# Update Employee
@employee_logger
@exception_handler
def update_employee(employee_id, employee):

    print("Inside update_employee()")

    employee_collection.update_one(
        {
            "_id": ObjectId(employee_id)
        },
        {
            "$set": employee
        }
    )

    print("Employee updated successfully")

    return {

        "message": "Employee Updated"

    }


# Delete Employee
@employee_logger
@exception_handler
def delete_employee(employee_id):

    print("Inside delete_employee()")

    employee_collection.delete_one(
        {
            "_id": ObjectId(employee_id)
        }
    )

    print("Employee deleted successfully")

    return {

        "message": "Employee Deleted"

    }