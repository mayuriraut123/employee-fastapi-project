import pandas as pd

from app.core.database import db


csv_collection = db["csv_employees"]



def save_csv(file):

    # Read CSV

    df = pd.read_csv(file.file)



    # Remove column spaces

    df.columns = df.columns.str.strip()



    inserted = 0

    duplicate_count = 0



    employees = []



    # Find duplicates inside CSV

    duplicate_rows = df[
        df.duplicated(
            subset=[
                "name",
                "department"
            ],
            keep="first"
        )
    ]


    duplicate_count += len(duplicate_rows)



    # Keep only first record

    df = df.drop_duplicates(
        subset=[
            "name",
            "department"
        ],
        keep="first"
    )



    for index, row in df.iterrows():


        employee = {

            "name": str(row["name"]).strip(),

            "age": int(row["age"]),

            "department": str(row["department"]).strip(),

            "salary": int(row["salary"])

        }



        # Check MongoDB duplicate

        existing = csv_collection.find_one(
            {
                "name": employee["name"],
                "department": employee["department"]
            }
        )



        if existing:

            duplicate_count += 1

            continue



        employees.append(employee)



    # Insert unique employees

    if employees:

        result = csv_collection.insert_many(
            employees
        )

        inserted = len(result.inserted_ids)



    return {

        "message": "Upload completed",

        "inserted_records": inserted,

        "duplicate_records": duplicate_count

    }