import functools


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