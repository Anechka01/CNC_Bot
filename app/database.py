from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    telegram_id = Column(Integer, unique=True, nullable=False)
    password = Column(String)


class Machine(Base):
    __tablename__ = "machine"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    name = Column(String)
    settings = Column(String)

class Setting(Base):
    __tablename__ = "setting"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(String)
    settings = Column(String)
    employee_id = Column(Integer, ForeignKey("employee.telegram_id"))
    machine_id = Column(Integer, ForeignKey("machine.id"))


SessionLocal = sessionmaker(autoflush=False, bind=engine)