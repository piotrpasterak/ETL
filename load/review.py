from datetime import datetime
from datetime import date
from load import *
from load.hotel import Hotel


class Review(db.Entity):
    """
    Represent Review entity from database.

    """
    _table_ = 'reviews'
    id = PrimaryKey(int, auto=True)
    hotel = Required(Hotel)
    rev_date = Required(datetime)
    name = Required(str)
    header = Required(str)
    country = Optional(str)
    info_tags = Optional(str)
    score = Required(float)
    stay_date = Optional(date)
    user_age_group = Optional(str)
    review_count = Required(int)
    neg_review = Optional(LongUnicode, nullable=True)
    pos_review = Optional(LongUnicode, nullable=True)

    def serialize_data(self):
        return [self.id,
                self.name,
                self.rev_date.strftime('%d-%m-%Y'),
                self.header,
                self.country,
                self.user_age_group,
                self.review_count,
                self.score,
                self.stay_date.strftime('%m-%Y'),
                self.info_tags,
                self.pos_review,
                self.neg_review]
