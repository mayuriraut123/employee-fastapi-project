import pandas as pd
import numpy as np

from fastapi import UploadFile, HTTPException

from app.core.database import db

csv_collection = db["csv_employees"]


def save_csv(file: UploadFile):

    try:

        df = pd.read_csv(file.file)

        df.columns = df.columns.str.strip()

        required_columns = [
            "name",
            "age",
            "department",
            "salary",
            "experience"
        ]

        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"{col} column not found."
                )

        # Fill Missing Values
        df.fillna(
            {
                "name": "",
                "age": 0,
                "department": "Unknown",
                "salary": 0,
                "experience": 0
            },
            inplace=True
        )

        # Remove Duplicate Records
        df = df.drop_duplicates(
            subset=["name", "department"],
            keep="first"
        )

        # Sort Salary
        df = df.sort_values(
            by="salary",
            ascending=False
        )

        # Top 5 Salary
        top5 = df.nlargest(
            5,
            "salary"
        )

        # Bottom 5 Salary
        bottom5 = df.nsmallest(
            5,
            "salary"
        )

        # Department Count
        department_count = (
            df["department"]
            .value_counts()
            .to_dict()
        )

        # Unique Department
        unique_department = (
            df["department"]
            .unique()
            .tolist()
        )

        # GroupBy
        group_summary = (

            df.groupby("department")

            .agg(

                Employee_Count=("name", "count"),

                Average_Salary=("salary", "mean"),

                Maximum_Salary=("salary", "max"),

                Minimum_Salary=("salary", "min")

            )

            .reset_index()

            .to_dict("records")

        )

        # Correlation
        correlation = (
            df[["age", "salary"]]
            .corr()
            .to_dict()
        )

        salary = np.array(df["salary"])

        experience = np.array(df["experience"])

        # Bonus
        df["bonus"] = salary * 0.10

        # Salary Category
        df["salary_category"] = np.where(
            salary >= 50000,
            "High",
            "Low"
        )

        # Employee Level
        df["level"] = np.select(

            [
                experience < 2,
                (experience >= 2) & (experience < 5),
                experience >= 5
            ],

            [
                "Junior",
                "Mid",
                "Senior"
            ],

            default="Unknown"

        )

        # Statistics
        average_salary = float(np.mean(salary))
        median_salary = float(np.median(salary))
        maximum_salary = float(np.max(salary))
        minimum_salary = float(np.min(salary))
        std_salary = float(np.std(salary))
        variance_salary = float(np.var(salary))
        percentile_salary = float(
            np.percentile(
                salary,
                90
            )
        )

        employees = df.to_dict("records")

        inserted = 0
        duplicate = 0

        employee_list = []

        for employee in employees:

            existing = csv_collection.find_one(

                {
                    "name": employee["name"],
                    "department": employee["department"]
                }

            )

            if existing:

                duplicate += 1

                continue

            employee_list.append(employee)

        if employee_list:

            result = csv_collection.insert_many(
                employee_list
            )

            inserted = len(result.inserted_ids)

        return {

            "message": "CSV Uploaded Successfully",

            "Inserted Records": inserted,

            "Duplicate Records": duplicate,

            "Average Salary": average_salary,

            "Median Salary": median_salary,

            "Maximum Salary": maximum_salary,

            "Minimum Salary": minimum_salary,

            "Standard Deviation": std_salary,

            "Variance": variance_salary,

            "90 Percentile Salary": percentile_salary,

            "Department Count": department_count,

            "Unique Department": unique_department,

            "Department Summary": group_summary,

            "Top 5 Salary": top5.to_dict("records"),

            "Bottom 5 Salary": bottom5.to_dict("records"),

            "Correlation": correlation

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )