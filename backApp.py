import datetime as datetime
import json

from database import *
import database as db
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Body, APIRouter, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse, FileResponse

# создаем таблицы
Base.metadata.create_all(bind=db.engine)
app = FastAPI()

def foo():
    pass


app.add_event_handler('start', foo)
app.add_event_handler('end', foo)


# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return FileResponse("public/index.html")


@app.get("/api/users")
def get_people(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@app.get("/api/users/{telegram_id}")
def get_person(telegram_id: int, db: Session = Depends(get_db)):
    # получаем пользователя по id
    person = db.query(Employee).filter(Employee.telegram_id == telegram_id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person is None:
        return False
    # если пользователь найден, отправляем его
    return person


@app.post("/api/users")
def create_employee(firstname: str, surname: str, telegram_id: int, password: str,  db: Session = Depends(get_db)):
    employee = Employee(first_name=firstname, second_name=surname, telegram_id=telegram_id, password = password)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return "Success"


@app.post("/api/machine")
def create_machine(data=Body(),  db: Session = Depends(get_db)):
    for k, v in data.items():
        for i, j in v.items():
            machine = Machine(type=k, name=i, settings=j)
            db.add(machine)
            db.commit()
            db.refresh(machine)
    return "Successful create list of machine"


@app.post("/api/machine2")
async def create_machine(request=Request,  db: Session = Depends(get_db)):
    data = await request.json()
    for k, v in data.items():
        for i, j in v.items():
            machine = Machine(type=k, name=i, settings=j)
            db.add(machine)
            db.commit()
            db.refresh(machine)
    return "Successful create list of machine"

@app.get("/api/machine")
def get_machine(name: str = "", db: Session = Depends(get_db)):
    if name:
        return db.query(Machine).filter(Machine.name == name).first()
    return db.query(Machine).all()

# @app.get("/api/machine")
# def get_machine(db: Session = Depends(get_db)):
#     return db.query(Machine).all()
#
# @app.get("/api/machine/{name}")
# def get_machine(name: str = "", db: Session = Depends(get_db)):
#     return db.query(Machine).filter(Machine.name == name).first()


@app.get("/api/auth")
def varify_psw(uid: int, password: str, db: Session = Depends(get_db)):
    db_psw = db.query(Employee).filter(Employee.telegram_id == uid).first()
    if db_psw.password == password:
        return True
    return False


@app.post("/api/setting", response_model=JSONResponse)
def set_setting(data=Body(), db: Session = Depends(get_db)):
    uid = data["uid"]
    settings = data["settings"]
    machine_id = data["machine_id"]
    time = data["datetime"]

    setting = Setting(datetime=time, settings=settings, employee_id=uid, machine_id=machine_id)
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return JSONResponse("Success process", status_code=status.HTTP_200_OK)
#
#
# @app.put("/api/users")
# def edit_person(data=Body(), db: Session = Depends(get_db)):
#     # получаем пользователя по id
#     person = db.query(Person).filter(Person.id == data["id"]).first()
#     # если не найден, отправляем статусный код и сообщение об ошибке
#     if person == None:
#         return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
#     # если пользователь найден, изменяем его данные и отправляем обратно клиенту
#     person.age = data["age"]
#     person.name = data["name"]
#     db.commit()  # сохраняем изменения
#     db.refresh(person)
#     return person
#
#
@app.delete("/api/users/{id}")
def delete_employee(telegram_id, db: Session = Depends(get_db)):
    # получаем пользователя по id
    person = db.query(Employee).filter(Employee.telegram_id == telegram_id).first()

    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})

    # если пользователь найден, удаляем его
    db.delete(person)  # удаляем объект
    db.commit()  # сохраняем изменения
    return person

