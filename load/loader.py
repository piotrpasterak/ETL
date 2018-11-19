from load import *
from transform import transformer
from extract import scrapper


if __name__ == '__main__':

    db.bind(provider='mysql', host='localhost', user='root', passwd='root', db='etl', charset='utf8mb4')
    #TODO: check if tables exist then call generate_mapping
    db.generate_mapping(create_tables=True)

    review = scrapper.scrap("http://www.booking.com/reviews/pl/hotel/cracowdayskrakow.html")

    trans = transformer.Transformer()

    with db_session:
        hotel = trans.transform_all(review)

    db.commit()



