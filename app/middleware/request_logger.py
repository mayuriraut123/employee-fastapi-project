import time

from fastapi import Request


async def request_logger(
    request: Request,
    call_next
):

    start_time = time.time()

    print("\n========== API REQUEST ==========")

    print(f"Method       : {request.method}")

    print(f"URL          : {request.url}")

    print(f"Client IP    : {request.client.host}")

    response = await call_next(request)

    end_time = time.time()

    process_time = end_time - start_time

    print(f"Status Code  : {response.status_code}")

    print(f"Time Taken   : {process_time:.4f} sec")

    print("=================================\n")

    return response