from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from src.routes import job_routes, user_routes
from src.utils.logger import setup_logger
from src.database import initialize_database

# Initialize logger
logger = setup_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Dynamic Job Matching Platform",
    description="An AI-powered platform for matching jobs with user profiles dynamically.",
    version="1.0.0"
)

# Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."},
    )

# Initialize database
initialize_database()

# Include routes
app.include_router(job_routes.router, prefix="/jobs", tags=["Jobs"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Dynamic Job Matching Platform API!"}

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)