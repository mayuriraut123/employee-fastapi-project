from bson import ObjectId
from app.core.database import employee_collection
from app.core.logger import logger


# Insert Employee
def insert_employee(employee):

    result = employee_collection.insert_one(employee)

    logger.info(
        f"Employee Added : {employee['name']}"
    )

    return {
        "message": "Employee Added",
        "id": str(result.inserted_id)
    }


# Get All Employees
def get_all_employees(
    page=1,
    limit=10,
    department=None
):

    employees = []

    skip = (page - 1) * limit

    query = {}

    # Filter by department
    if department:
        query["department"] = department

    total = employee_collection.count_documents(query)

    result = employee_collection.find(query).skip(skip).limit(limit)

    for employee in result:

        employee["_id"] = str(employee["_id"])

        employees.append(employee)

    logger.info(
        f"Employee List Viewed | Page={page} | Limit={limit} | Department={department}"
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": employees
    }


# Get One Employee
def get_employee(employee_id):

    employee = employee_collection.find_one(
        {"_id": ObjectId(employee_id)}
    )

    if employee:

        employee["_id"] = str(employee["_id"])

        logger.info(
            f"Employee Viewed : {employee_id}"
        )

        return employee

    logger.error(
        f"Employee Not Found : {employee_id}"
    )

    return {
        "message": "Employee Not Found"
    }


# Update Employee
def update_employee(employee_id, employee):

    employee_collection.update_one(
        {"_id": ObjectId(employee_id)},
        {"$set": employee}
    )

    logger.info(
        f"Employee Updated : {employee_id}"
    )

    return {
        "message": "Employee Updated"
    }


# Delete Employee
def delete_employee(employee_id):

    employee_collection.delete_one(
        {"_id": ObjectId(employee_id)}
    )

    logger.info(
        f"Employee Deleted : {employee_id}"
    )

    return {
        "message": "Employee Deleted"
    }