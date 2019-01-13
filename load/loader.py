"""Load data to database module.

This module implements 'load' to database functionality, in this particular case it update content of etl database.
Mainly Pony ORM web drive is in use.

.. Pony ORM site:
   https://ponyorm.com/
"""

from load.hotel import Hotel
from load.review import Review
from load import *


def init_connection():
    """Initialize default connection to database, and create tables if necessary.

    """

    db.bind(provider='mysql', host='localhost', user='root', passwd='root', db='etl', charset='utf8mb4')
    db.generate_mapping(create_tables=True)


def generate_raw_filer(filter_dic):
    if len(filter_dic) == 0:
        return ""

    result_sql = ""
    for key, value in filter_dic.items():
        if value and len(value) != 0:
            result_sql += " AND " + key + ' LIKE ' + "\'" + value + "\'"
    return result_sql


@db_session
def get_data_for_hotel(hotel_name, filter):
    """If all reviews from hotel are necessary.

    Args:
        hotel_name (str): The name of the Hotel.

    Returns:
        list of serialized data from Reviews of None if no data or no such Hotel.
    """
    loc_hotel = Hotel.get(name=hotel_name)
    if loc_hotel is None:
        return None
    else:
        raw_sql_filter = generate_raw_filer(filter)
        if len(raw_sql_filter) == 0:
            return [rev.serialize_data() for rev in loc_hotel.reviews]
        else:
            sqlquery = "SELECT * FROM reviews WHERE reviews.hotel = " + str(loc_hotel.id)
            sqlquery += raw_sql_filter
            revlist = Review .select_by_sql(sqlquery)
            return [rev.serialize_data() for rev in revlist]


@db_session
def clear_data_for_hotel(hotel_name):
    """Deletes all reviews linked to Hotel.

    Args:
        hotel_name (str): The name of the Hotel.
    """
    loc_hotel = Hotel.get(name=hotel_name)
    if loc_hotel:
        delete(rev for rev in Review if rev.hotel.id == loc_hotel.id)


@db_session
def get_all_hotels():
    """Gives all hotels from database.

    Returns:
        List of all Hotels (objects).
    """
    hotels = select(hotel for hotel in Hotel)
    return hotels.fetch()


@db_session
def update_hotel_with_data(hotel_data):
    """Just clean all data if so, and create new Review entities in database.

    Args:
        hotel_data: The dictionary with all hotel data (also connected Reviews).
    """
    loc_hotel = Hotel.get(name=hotel_data["name"])
    obj_count = 0

    if loc_hotel is None:
        loc_hotel = Hotel(name=hotel_data["name"], address=hotel_data["address"])
        obj_count += 1
    else:
        clear_data_for_hotel(loc_hotel.name)

    for review_data in hotel_data["review"]:
        Review(hotel=loc_hotel,
               name=review_data['name'],
               date=review_data['date'],
               header=review_data['header'],
               country=review_data['country'],
               user_age_group=review_data['user_age_group'],
               review_count=review_data['review_count'],
               score=review_data['score'],
               info_tags=review_data['info_tags'],
               pos_review=review_data['pos_review'],
               neg_review=review_data['neg_review'])
        obj_count += 1
    return obj_count




