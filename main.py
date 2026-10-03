import os
import time
from datetime import datetime, date
from fastapi import FastAPI, HTTPException, Depends
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, extract
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi.responses import FileResponse

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./attendance.db")
args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=args)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    emp_id = Column(Integer, nullable=False, index=True)
    day = Column(Date, nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime)


# Wait for the database to be ready (useful on Kubernetes)
for _ in range(10):
    try:
        Base.metadata.create_all(engine)
        break
    except Exception:
        time.sleep(3)

app = FastAPI(title="Attendance System")
Instrumentator().instrument(app).expose(app)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fmt(t):
    return t.strftime("%H:%M:%S") if t else None


@app.get("/")
def home():
    return {"message": "Attendance System  v5 is running"}


@app.post("/employees")
def add_employee(name: str, db: Session = Depends(get_db)):
    emp = Employee(name=name)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return {"id": emp.id, "name": emp.name}


@app.get("/employees")
def list_employees(db: Session = Depends(get_db)):
    return [{"id": e.id, "name": e.name} for e in db.query(Employee).all()]


@app.post("/check-in/{emp_id}")
def check_in(emp_id: int, db: Session = Depends(get_db)):
    if not db.get(Employee, emp_id):
        raise HTTPException(404, "Employee not found")
    if db.query(Attendance).filter_by(emp_id=emp_id, day=date.today()).first():
        raise HTTPException(400, "Already checked in today")
    db.add(Attendance(emp_id=emp_id, day=date.today(), check_in=datetime.now()))
    db.commit()
    return {"message": "Checked in"}


@app.post("/check-out/{emp_id}")
def check_out(emp_id: int, db: Session = Depends(get_db)):
    rec = db.query(Attendance).filter_by(emp_id=emp_id, day=date.today()).first()
    if not rec:
        raise HTTPException(400, "You have not checked in today")
    rec.check_out = datetime.now()
    db.commit()
    return {"message": "Checked out"}


@app.get("/report/today")
def report_today(db: Session = Depends(get_db)):
    rows = db.query(Attendance, Employee).join(
        Employee, Employee.id == Attendance.emp_id
    ).filter(Attendance.day == date.today()).all()
    return [
        {"emp_id": e.id, "name": e.name, "day": str(a.day),
         "check_in": fmt(a.check_in), "check_out": fmt(a.check_out)}
        for a, e in rows
    ]


@app.get("/report/monthly")
def report_monthly(year: int, month: int, db: Session = Depends(get_db)):
    rows = db.query(Attendance, Employee).join(
        Employee, Employee.id == Attendance.emp_id
    ).filter(
        extract("year", Attendance.day) == year,
        extract("month", Attendance.day) == month,
    ).all()
    summary = {}
    for a, e in rows:
        summary[e.name] = summary.get(e.name, 0) + 1
    return {"year": year, "month": month, "days_present": summary}

@app.get("/app")
def frontend():
    return FileResponse("static/index.html")