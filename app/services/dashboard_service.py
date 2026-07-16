from app.core.database import db


employee_collection = db["employees"]



# Total Employee Count

def total_employee():

    count = employee_collection.count_documents({})

    return {
        "total_employee": count
    }



# Department Wise Count

def department_count():

    result = employee_collection.aggregate(
        [
            {
                "$group":
                {
                    "_id":"$department",
                    "count":{
                        "$sum":1
                    }
                }
            }
        ]
    )


    data = []

    for row in result:

        data.append(
            {
                "department":row["_id"],
                "count":row["count"]
            }
        )


    return data




# Average Salary

def average_salary():

    result = employee_collection.aggregate(
        [
            {
                "$group":
                {
                    "_id": None,
                    "average_salary":
                    {
                        "$avg": "$salary"
                    }
                }
            }
        ]
    )


    data = list(result)


    if data and data[0].get("average_salary") is not None:

        return {
            "average_salary": round(
                data[0]["average_salary"],
                2
            )
        }


    return {
        "average_salary": 0
    }



# Highest Salary Employee

def highest_salary():

    result = employee_collection.find_one(
        {},
        sort=[
            (
                "salary",
                -1
            )
        ]
    )


    if result:

        result["_id"]=str(
            result["_id"]
        )
        return result


    return {}