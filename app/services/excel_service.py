import pandas as pd
import numpy as np

from fastapi import UploadFile, HTTPException

from app.core.database import db

excel_collection = db["excel_employees"]


def save_excel(file: UploadFile):

    try:

        # Read Excel
        df = pd.read_excel(
            file.file,
            engine="openpyxl"
        )

        # Remove extra spaces from column names
        df.columns = df.columns.str.strip()

        # Required columns
        required_columns = [
            "name",
            "age",
            "department",
            "salary"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing columns: {', '.join(missing)}"
            )

        # Fill missing values
        df.fillna(
            {
                "name": "",
                "age": 0,
                "department": "Unknown",
                "salary": 0
            },
            inplace=True
        )

        # Remove duplicates
        df = df.drop_duplicates(
            subset=["name", "department"],
            keep="first"
        )

        # Sort by salary
        df = df.sort_values(
            by="salary",
            ascending=False
        )

        # Top 5
        top5 = df.nlargest(
            5,
            "salary"
        )

        # Bottom 5
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

        # Unique Departments
        unique_departments = (
            df["department"]
            .unique()
            .tolist()
        )

        # GroupBy
        group_summary = (

            df.groupby("department")

            .agg(

                Total_Employees=("name", "count"),

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

        # NumPy Array
        salary = np.array(df["salary"])

        # Bonus
        df["bonus"] = salary * 0.10

        # Salary Category
        df["salary_category"] = np.where(
            salary >= 50000,
            "High",
            "Low"
        )

        # Experience Column (Optional)
        if "experience" in df.columns:

            experience = np.array(df["experience"])

            df["level"] = np.select(

                [
                    experience < 2,
                    experience < 5,
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

        percentile90 = float(
            np.percentile(
                salary,
                90
            )
        )

        # Convert to dictionary
        employees = df.to_dict("records")

        inserted = 0
        duplicate = 0

        employee_list = []

        for employee in employees:

            existing = excel_collection.find_one(
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

            result = excel_collection.insert_many(
                employee_list
            )

            inserted = len(result.inserted_ids)

        return {

            "message": "Excel Uploaded Successfully",

            "Inserted Records": inserted,

            "Duplicate Records": duplicate,

            "Average Salary": average_salary,

            "Median Salary": median_salary,

            "Maximum Salary": maximum_salary,

            "Minimum Salary": minimum_salary,

            "Standard Deviation": std_salary,

            "Variance": variance_salary,

            "90 Percentile Salary": percentile90,

            "Department Count": department_count,

            "Unique Departments": unique_departments,

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