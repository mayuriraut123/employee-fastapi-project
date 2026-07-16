from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")

# Select Database
db = client["EmployeeDB"]

# Select Collection
employee_collection = db["employees"]