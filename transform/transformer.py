from extract import scrapper
from datetime import datetime
import locale


class Review:
    '''Review class contains all collected data'''
    def __init__(self, hml_review):

        self.date = Review.extract_date(hml_review)
        self.name = Review.extract_name(hml_review)
        self.country = Review.extract_country(hml_review)
        self.user_age_group = Review.extract_user_age_group(hml_review)
        self.review_count = Review.extract_user_age_group(hml_review)
        self.score = Review.extract_score(hml_review)
        self.header = Review.extract_header(hml_review)
        #TODO review_item_info_tags
        self.pos_review = Review.extract_pos_review_body(hml_review)
        self.neg_review = Review.extract_neg_review_body(hml_review)

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
        return review_count

    @staticmethod
    def extract_score(hml_review):
        '''reviewer score extraction method'''
        score = hml_review.find("span", {"class": "review-score-badge"}).get_text(strip=True)
        return score
        
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


def transform(html_review_list):
    '''main transform method'''
    db_reviews = []

    for html_review_sublist in html_review_list:
        for html_review in html_review_sublist:
            db_reviews.append(Review(html_review))

    return db_reviews


if __name__ == '__main__':

    data = transform(scrapper.scrap("http://www.booking.com/reviews/pl/hotel/cracowdayskrakow.html"))

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



