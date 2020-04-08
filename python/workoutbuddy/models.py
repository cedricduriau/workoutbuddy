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
    sets = relationship("ExerciseSet", back_populates="exercise")


class ExerciseSet(Base):
    __tablename__ = "exercisesets"

    id = Column(Integer, primary_key=True)
    reps = Column(Integer, unique=False, nullable=False)

    # relationships
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    exercise = relationship("Exercise", back_populates="sets")
    logs = relationship("Log", back_populates="exercise_set")


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    date = Column(Date, unique=False, nullable=False)

    # relationships
    exercise_set_id = Column(Integer, ForeignKey("exercisesets.id"))
    exercise_set = relationship("ExerciseSet", back_populates="logs")
