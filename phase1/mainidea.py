
from typing import Annotated

from fastapi import (
    FastAPI,
    Path,
    Query,
    Body,
    Header,
    Cookie,
    Form,
    File,
    UploadFile,
    Depends,
    Request,
    Response,
    HTTPException,
)
from pydantic import BaseModel

app = FastAPI(title="FastAPI Parameters Demo")


# 1. Pydantic model: JSON request body
class Employee(BaseModel):
    name: str
    age: int
    department: str


# 2. Dependency: reusable function
def get_current_user():
    return {"username": "vishal", "role": "admin"}


# 3. PATH + QUERY + HEADER + COOKIE + DEPENDS
@app.get("/employees/{employee_id}")
def get_employee(
    # Path parameter
    employee_id: Annotated[int, Path(ge=1)],

    # Query parameters
    search: Annotated[str | None, Query(min_length=2)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,

    # Header parameter
    user_agent: Annotated[str | None, Header()] = None,

    # Cookie parameter
    session_id: Annotated[str | None, Cookie()] = None,

    # Dependency injection
    current_user: Annotated[dict, Depends(get_current_user)] = None,

    # Request object
    request: Request = None,

    # Response object
    response: Response = None,
):
    response.headers["X-App-Name"] = "FastAPI-Demo"

    return {
        "employee_id": employee_id,
        "search": search,
        "limit": limit,
        "user_agent": user_agent,
        "session_id": session_id,
        "current_user": current_user,
        "http_method": request.method,
    }


# 4. BODY: JSON + PATH + QUERY
@app.post("/employees/{employee_id}")
def create_employee(
    employee_id: Annotated[int, Path(ge=1)],
    employee: Employee,
    active: bool = True,
):
    return {
        "message": "Employee received",
        "employee_id": employee_id,
        "employee": employee,
        "active": active,
    }


# 5. BODY: explicit scalar fields
@app.post("/calculate")
def calculate(
    price: Annotated[float, Body(gt=0)],
    quantity: Annotated[int, Body(ge=1)],
):
    return {"total": price * quantity}


# 6. FORM parameters
@app.post("/login")
def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    # Demo only: never return or log passwords in production.
    return {
        "username": username,
        "message": "Form received",
    }


# 7. FILE upload
@app.post("/upload")
async def upload_file(
    file: Annotated[UploadFile, File()],
):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }


# 8. REQUEST object
@app.get("/request-info")
async def request_info(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "user_agent": request.headers.get("user-agent"),
    }


# 9. RESPONSE object
@app.get("/custom-response")
def custom_response(response: Response):
    response.headers["X-Custom-Header"] = "Hello"
    response.status_code = 200

    return {"message": "Custom response created"}


# 10. DELETE + PATH + QUERY
@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: Annotated[int, Path(ge=1)],
    permanent: bool = False,
):
    return {
        "message": "Delete request received",
        "employee_id": employee_id,
        "permanent": permanent,
    }
