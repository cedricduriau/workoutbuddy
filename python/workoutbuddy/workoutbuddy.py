# stdlib modules
import os
import datetime

# tool modules
from workoutbuddy.models import Base
from workoutbuddy.models import Exercise
from workoutbuddy.models import Log

# third party modules
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


CACHE_DIR = os.path.expanduser("~/.workoutbuddy")
DB_PATH = os.path.join(CACHE_DIR, "workoutbuddy.db")


# =============================================================================
# private
# =============================================================================
def _create_engine():
    """
    Create an SQLAlchemy database engine.

    :rtype: sqlalchemy.engine.Engine
    """
    engine_url = "sqlite:///{}".format(DB_PATH)
    engine = create_engine(engine_url)
    return engine


def _record_to_dict(r):
    """
    Build a dictionary from a database record.

    :param r: Datbase record.
    :type r: sqlalchemy.engine.result.ResultMetaData

    :rtype: dict
    """
    return dict(zip(r.keys(), r))


def _get_records(table):
    """
    Return all records of a database table.

    :param table: SQLAlchemy table model.
    :type table: Base

    :rtype: list[sqlalchemy.engine.result.ResultMetaData]
    """
    session = create_session()
    query = select("*").select_from(table)
    result = session.execute(query).fetchall()
    return result


def _list_records(table):
    """
    Print all records of a database table.

    :param table: SQLAlchemy table model.
    :type table: Base
    """
    records = _get_records(table)
    dicts = list(map(_record_to_dict, records))
    for d in dicts:
        print(d)


# =============================================================================
# public
# =============================================================================
def create_session():
    """
    Create a database session.

    :rtype: sqlalchemy.orm.session.Session
    """
    engine = _create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def set_up():
    """Set up the database and tables."""
    engine = _create_engine()
    Base.metadata.create_all(engine)


def tear_down():
    """Drop all database records."""
    engine = _create_engine()
    Base.metadata.drop_all(engine)
    set_up()


def list_exercises():
    """List all exercise database records."""
    _list_records(Exercise)


def list_logs():
    """List all exercise log records."""
    _list_records(Log)


def create_exercise(name):
    """
    Create an exercise.

    :param name: Name of the exercise.
    :type name: str

    :rtype: Exercise
    """
    session = create_session()

    exercise = session.query(Exercise).filter(Exercise.name == name).first()
    if exercise:
        print("exercise already exists (id: {})".format(exercise.id))
        return

    exercise = Exercise(name=name)
    session.add(exercise)
    session.commit()
    return exercise


def log_exercise(date, exerciseid, reps):
    """
    Log an exercise.

    :param date: Date of the performed exercise.
                 Format DD/MM/YYYY. Use 'today' for current date.
    :type date: str

    :param exerciseid: ID of the exercise to log.
    :type exerciseid: int

    :param reps: Amount of repetitions.
    :type reps: int

    :rtype: Log
    """
    if date == "today":
        date = datetime.date.today()
    else:
        date = datetime.datetime.strptime(date, "%d/%m/%Y")

    session = create_session()
    exercise = session.query(Exercise).filter(Exercise.id == exerciseid).first()
    if not exercise:
        print("no exercise found for id: {}".format(exercise.id))
        return

    log = Log(date=date, exercise=exercise, reps=reps)
    session.add(log)
    session.commit()
    return log
