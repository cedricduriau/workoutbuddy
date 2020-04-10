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
    Creates an SQLAlchemy database engine.

    :rtype: Engine
    """
    engine_url = f"sqlite:///{DB_PATH}"
    engine = create_engine(engine_url)
    return engine


def _record_to_dict(r):
    return dict(zip(r.keys(), r))


def _get_records(table):
    session = create_session()
    query = select("*").select_from(table)
    result = session.execute(query).fetchall()
    return result


def _list_records(table):
    records = _get_records(table)
    dicts = list(map(_record_to_dict, records))
    for d in dicts:
        print(d)


# =============================================================================
# public
# =============================================================================
def create_session():
    engine = _create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def set_up():
    engine = _create_engine()
    Base.metadata.create_all(engine)


def tear_down():
    engine = _create_engine()
    Base.metadata.drop_all(engine)
    set_up()


def list_exercises():
    _list_records(Exercise)


def list_logs():
    _list_records(Log)


def create_exercise(name):
    session = create_session()

    exercise = session.query(Exercise).filter(Exercise.name == name).first()
    if exercise:
        print(f"exercise already exists (id: {exercise.id})")
        return

    exercise = Exercise(name=name)
    session.add(exercise)
    session.commit()
    return exercise


def log_exercise(date, exerciseid, reps):
    if date == "today":
        date = datetime.date.today()
    else:
        date = datetime.datetime.strptime(date, "%d/%m/%Y")

    session = create_session()
    exercise = session.query(Exercise).filter(Exercise.id == exerciseid).first()
    if not exercise:
        print(f"no exercise found for id: {exercise.id}")
        return

    log = Log(date=date, exercise=exercise, reps=reps)
    session.add(log)
    session.commit()
    return log
