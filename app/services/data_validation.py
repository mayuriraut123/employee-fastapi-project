import pandas as pd



required_columns = [
    "name",
    "age",
    "department",
    "salary"
]



def validate_employee_data(df):

    errors = []


    # Check columns

    for column in required_columns:

        if column not in df.columns:

            errors.append(
                f"Missing column {column}"
            )


    if errors:

        return False, errors



    # Check empty values

    for index,row in df.iterrows():

        if pd.isna(row["name"]):

            errors.append(
                f"Row {index}: Name missing"
            )


        if pd.isna(row["age"]):

            errors.append(
                f"Row {index}: Age missing"
            )



    # Check datatype

    for index,row in df.iterrows():

        try:

            int(row["age"])

        except:

            errors.append(
                f"Row {index}: Invalid age"
            )



        try:

            int(row["salary"])

        except:

            errors.append(
                f"Row {index}: Invalid salary"
            )


    if errors:

        return False, errors



    return True, []