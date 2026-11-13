from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from models import Employee
from schemas import EmpolyeeRequest, EmployeeResponse
from database import get_db, Session, engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.post("/addemp")
def add_employee(employee: EmpolyeeRequest, db: Session = Depends(get_db)):

    user_detail = db.query(Employee).all()

    if employee in user_detail:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        age=employee.age,
        date=employee.date
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
        "message": "Employee added successfully",
        "employee": {
            "id": new_employee.id,
            "name": new_employee.name,
            "email": new_employee.email,
            "age": new_employee.age,
            "date": str(new_employee.date)
        }
    }


@app.get("/getemp")
def get_employee(db: Session = Depends(get_db)):

    user_detail = db.query(Employee).all()
    if not user_detail:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return user_detail

# var = get_db()
# @app.get("/getemp")
# def get_employee(db: var):

#     user_detail = db.query(Employee).all()
#     if not user_detail:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

#     return user_detail


@app.put("/update/{emp_id}")
def update_employee(emp_id: int, updated_data: EmpolyeeRequest, db: Session = Depends(get_db)):

    user_detail = db.query(Employee).filter(Employee.id == emp_id).first()

    if not user_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    user_detail.name=updated_data.name,
    user_detail.email=updated_data.email,
    user_detail.age=updated_data.age,
    user_detail.date=updated_data.date

    db.commit()
    db.refresh(user_detail)
    return {"message": "Item Successfully Updated"}



