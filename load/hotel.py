from load import *


class Hotel(db.Entity):
    _table_ = 'hotels'
    id = PrimaryKey(int, auto=True)
    name = Optional(str, unique=True)
    reviews = Set('Review')
    address = Required(str)
