from load.hotel import Hotel
from load.review import Review
from load import *


def init_connection():
    db.bind(provider='mysql', host='localhost', user='root', passwd='root', db='etl', charset='utf8mb4')
    db.generate_mapping(create_tables=True)


@db_session
def get_data_for_hotel(hotel_name):
    pass


@db_session
def clear_data_for_hotel(hotel_id):
    delete(rev for rev in Review if rev.hotel.id == hotel_id)


@db_session
def get_all_hotels():
    pass


@db_session
def update_hotel_with_data(hotel_data):
    loc_hotel = Hotel.get(name=hotel_data["name"])

    if loc_hotel is None:
        loc_hotel = Hotel(name =hotel_data["name"], address = hotel_data["address"])
    else:
        clear_data_for_hotel(loc_hotel.id)

    for review_data in hotel_data["review"]:
        Review(hotel=loc_hotel,
               name=review_data['name'],
               date=review_data['date'],
               header = review_data['header'],
               country = review_data['country'],
               user_age_group = review_data['user_age_group'],
               review_count = review_data['review_count'],
               score = review_data['score'],
               # TODO review_item_info_tags,
               pos_review = review_data['pos_review'],
               neg_review = review_data['neg_review'])





