import functools

from bson.errors import InvalidId
from pymongo.errors import PyMongoError


def employee_logger(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        print("\n===================================")
        print(f"Calling API : {func.__name__}")
        print("===================================")

        result = func(*args, **kwargs)

        print("===================================")
        print(f"Completed API : {func.__name__}")
        print("===================================\n")

        return result

    return wrapper


def exception_handler(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        try:

            return func(*args, **kwargs)

        except InvalidId:

            return {
                "success": False,
                "message": "Invalid Employee ID"
            }

        except PyMongoError as e:

            print(f"Database Error : {e}")

            return {
                "success": False,
                "message": "Database Error"
            }

        except Exception as e:

            print(f"Unexpected Error : {e}")

            return {
                "success": False,
                "message": "Internal Server Error"
            }

    return wrapper