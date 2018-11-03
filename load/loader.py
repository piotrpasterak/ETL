from pony.orm import Database
from pony.orm import DBException


def connect_to_database():
    db = Database()

    try:
        db.bind()
    except DBException as e:
        print(e)
