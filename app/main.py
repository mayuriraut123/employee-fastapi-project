from fastapi import FastAPI, Request

from app.routers.auth import router as auth_router
from app.routers.employee import router as employee_router
from app.routers.csv_upload import router as csv_router
from app.routers.excel_upload import router as excel_router
from app.routers.dashboard import router as dashboard_router

from app.core.logger import logger


# Create FastAPI app
app = FastAPI(
    title="Employee API"
)


# -----------------------------
# Logging Middleware
# -----------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):

    logger.info(
        f"Request : {request.method} {request.url.path}"
    )

    response = await call_next(request)

    logger.info(
        f"Response : {response.status_code}"
    )

    return response


# -----------------------------
# Register Routers
# -----------------------------
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(csv_router)
app.include_router(excel_router)
app.include_router(dashboard_router)


# -----------------------------
# Home API
# -----------------------------
@app.get("/")
def home():

    logger.info("Home API Called")

    return {
        "message": "Employee API Running"
    }