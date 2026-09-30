from datetime import datetime, date
from fastapi import FastAPI, HTTPException

app = FastAPI()

employees = {}      # stores employees: {1: "Ali", 2: "Sara"}
attendance = []     # stores check-in/out records

@app.get("/")
def home():
    return {"message": "Attendance System is running"}

@app.post("/employees")
def add_employee(name: str):
    emp_id = len(employees) + 1
    employees[emp_id] = name
    return {"id": emp_id, "name": name}

@app.post("/check-in/{emp_id}")
def check_in(emp_id: int):
    if emp_id not in employees:
        raise HTTPException(404, "Employee not found")
    for r in attendance:
        if r["emp_id"] == emp_id and r["day"] == str(date.today()):
            raise HTTPException(400, "Already checked in today")
    attendance.append({
        "emp_id": emp_id,
        "name": employees[emp_id],
        "day": str(date.today()),
        "check_in": datetime.now().strftime("%H:%M:%S"),
        "check_out": None,
    })
    return {"message": "Checked in"}

@app.post("/check-out/{emp_id}")
def check_out(emp_id: int):
    for r in attendance:
        if r["emp_id"] == emp_id and r["day"] == str(date.today()):
            r["check_out"] = datetime.now().strftime("%H:%M:%S")
            return {"message": "Checked out"}
    raise HTTPException(400, "You have not checked in today")

@app.get("/report/today")
def report_today():
    return [r for r in attendance if r["day"] == str(date.today())]