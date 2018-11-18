from datetime import datetime
from pony.orm import *
import pymysql

db = Database()


class Hotel(db.Entity):
    _table_ = 'Hotels'
    id = PrimaryKey(int, auto=True)
    name = Optional(str, unique=True)
    reviews = Set('Review')
    address = Required(str)


class Review(db.Entity):
    _table_ = 'Reviews'
    id = PrimaryKey(int, auto=True)
    hotel = Required(Hotel)
    date = Required(datetime)
    name = Required(str, unique=True)
    header = Required(str)
    country = Required(str)
    score = Required(str)
    user_age_group = Required(str)
    review_count = Required(str)
    neg_review = Optional(str, nullable=True)
    pos_review = Optional(str, nullable=True)


if __name__ == '__main__':
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='root')

   # try:
       # conn.cursor().execute('create database etl')
    #except ProgrammingError as e:
     #   print(e)

    db.bind(provider='mysql', host='localhost', user='root', passwd='root', db='etl')
    db.generate_mapping(create_tables=True)
