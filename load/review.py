from datetime import datetime
from load import *
from load.hotel import Hotel


class Review(db.Entity):
    _table_ = 'Reviews'
    id = PrimaryKey(int, auto=True)
    hotel = Required(Hotel)
    date = Required(datetime)
    name = Required(str)
    header = Required(str)
    country = Required(str)
    score = Required(float)
    user_age_group = Optional(str)
    review_count = Required(int)
    neg_review = Optional(LongUnicode , nullable=True)
    pos_review = Optional(LongUnicode , nullable=True)
