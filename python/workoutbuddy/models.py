# third party modules
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

    # relationships
    logs = relationship("Log", back_populates="exercise")


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    date = Column(Date, unique=False, nullable=False)
    reps = Column(Integer, unique=False, nullable=False)

    # relationships
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    exercise = relationship("Exercise", back_populates="logs")
