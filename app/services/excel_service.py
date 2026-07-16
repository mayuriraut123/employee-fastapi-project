import pandas as pd
import numpy as np

from app.core.database import db


excel_collection = db["excel_employees"]



def save_excel(file):

    # Read Excel file

    df = pd.read_excel(
        file.file
    )



    # Remove column spaces

    df.columns = df.columns.str.strip()



    inserted = 0

    duplicate_count = 0



    employees = []



    # Check duplicate inside Excel

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



    # Keep only first occurrence

    df = df.drop_duplicates(
        subset=[
            "name",
            "department"
        ],
        keep="first"
    )



    # Convert dataframe to numpy

    data = np.array(df)



    for row in data:


        employee = {

            "name": str(row[0]).strip(),

            "age": int(row[1]),

            "department": str(row[2]).strip(),

            "salary": int(row[3])

        }



        # Check MongoDB duplicate

        existing = excel_collection.find_one(
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

        result = excel_collection.insert_many(
            employees
        )

        inserted = len(result.inserted_ids)



    return {

        "message":"Excel upload completed",

        "inserted_records":inserted,

        "duplicate_records":duplicate_count

    }