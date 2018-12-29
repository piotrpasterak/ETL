from extract import scrapper
from datetime import datetime
from load.hotel import Hotel
from load.review import Review


class Transformer:
    '''Review class contains all collected data'''
    def __init__(self):
        pass

    @staticmethod
    def transform_all(html_review_list):
        '''main transform method'''

        hotel = Hotel(name="Cracowdays", address="ul. Grabowskiego 7/2, Old Town, 31-126 Krakow, Poland")

        for html_review_sublist in html_review_list:
            for html_review in html_review_sublist:
                Review(hotel= hotel,
                       name = Transformer.extract_name(html_review),
                       date = Transformer.extract_date(html_review),
                       header=Transformer.extract_header(html_review),
                       country= Transformer.extract_country(html_review),
                       user_age_group =Transformer.extract_user_age_group(html_review),
                       review_count = Transformer.extract_review_count(html_review),
                       score = Transformer.extract_score(html_review),
        #TODO review_item_info_tags,
                       pos_review=Transformer.extract_pos_review_body(html_review),
                       neg_review=Transformer.extract_neg_review_body(html_review))

        return hotel

    @staticmethod
    def transfom_hotels(raw_hotels_list):
        hotels = {}

        for raw_hotel in raw_hotels_list:
            hotels[Transformer.extract_hotel_name(raw_hotel)] = Transformer.extract_hotel_link(raw_hotel)
        return hotels

    @staticmethod
    def extract_hotel_name(raw_hotel):
        return raw_hotel.find("span", {"class": "sr-hotel__name "}).get_text(strip=True)
    @staticmethod
    def extract_hotel_link(raw_hotel):
        return 'ala'#raw_hotel.find("a", {"class": "hotel_name_link url"}).get_attr("href")

    @staticmethod
    def extract_date(hml_review):
        '''review put date extraction method'''
        date_raw = hml_review.find("p", {"class": "review_item_date"}).get_text(strip=True)
        date = datetime.strptime(date_raw, 'Reviewed: %d %B %Y')
        return date

    @staticmethod
    def extract_name(hml_review):
        '''reviewer name extraction method'''
        name_part = hml_review.find("p", {"class": "reviewer_name"})
        name = name_part.find("span", {"itemprop": "name"}).get_text(strip=True)
        return name

    @staticmethod
    def extract_country(hml_review):
        '''reviewer coutry extraction method'''
        country_part = hml_review.find("span", {"class": "reviewer_country"})
        country = country_part.find("span", {"itemprop": "name"}).get_text(strip=True)
        return country

    @staticmethod
    def extract_user_age_group(hml_review):
        '''reviewer age group extraction method'''
        age_group = hml_review.find("div", {"class": "user_age_group"}).get_text(strip=True)
        return age_group
        
    @staticmethod
    def extract_review_count(hml_review):
        '''reviewer review count extraction method'''
        review_count = hml_review.find("div", {"class": "review_item_user_review_count"}).get_text(strip=True)
        numbers = [int(count) for count in review_count.split() if count.isdigit()]
        return numbers[0]

    @staticmethod
    def extract_score(hml_review):
        '''reviewer score extraction method'''
        score = hml_review.find("span", {"class": "review-score-badge"}).get_text(strip=True)
        return float(score)
        
    @staticmethod
    def extract_header(hml_review):
        '''review header extraction method'''
        header_part = hml_review.find("div", {"class": "review_item_header_content "})
        header = header_part.find("span", {"itemprop": "name"}).get_text(strip=True)
        return header

    @staticmethod
    def extract_neg_review_body(hml_review):
        '''negative review extraction method'''
        neg_body = None
        neg_body_text = None

        review_neg = hml_review.find("p", {"class": "review_neg "})
        if review_neg is not None:
            neg_body = review_neg.find("span", {"itemprop": "reviewBody"})
        if neg_body is not None:
            neg_body_text=neg_body.get_text(strip=True)
        return neg_body_text

    @staticmethod
    def extract_pos_review_body(hml_review):
        '''positive review extraction method'''
        pos_body = None
        pos_body_text = None

        review_pos = hml_review.find("p", {"class": "review_pos "})
        if review_pos is not None:
            pos_body = review_pos.find("span", {"itemprop": "reviewBody"})
        if pos_body is not None:
            pos_body_text=pos_body.get_text(strip=True)
        return pos_body_text


if __name__ == '__main__':

    data = Transformer.transform_all(scrapper.scrap("http://www.booking.com/reviews/pl/hotel/cracowdayskrakow.html"))

    for review in data:
        print(review.date)
        print(review.name)
        print(review.header)
        print(review.country)
        print(review.score)
        print(review.user_age_group)
        print(review.review_count)
        print(review.neg_review)
        print(review.pos_review)



