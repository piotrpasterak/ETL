"""Adapting data into format accepted by database module.

This module implements 'transform' functionality (as a part of ETL model).
Data are Extract module and Load module is receiver of adapted data.
"""
from datetime import datetime


class Transformer:
    """Review class contains all necessary operations.
    """
    def __init__(self):
        pass

    @staticmethod
    def transform_all(html_review_list, hotel_name, hotel_address):
        """Main transforming method'.

        Args:
            html_review_list (str): HTML content of Reviews.
            hotel_name (str): Name of the hotel.

        Returns:
            Hotel dictionary with data.

        """

        hotel = {"name": hotel_name, "address": hotel_address, 'review': []}

        for html_review in html_review_list:
            hotel["review"].append({"name": Transformer.extract_name(html_review),
                                    "date": Transformer.extract_date(html_review),
                                    "header" :Transformer.extract_header(html_review),
                                    "country": Transformer.extract_country(html_review),
                                    "user_age_group": Transformer.extract_user_age_group(html_review),
                                    "review_count": Transformer.extract_review_count(html_review),
                                    "score": Transformer.extract_score(html_review),
                                    "info_tags":  Transformer.extract_info_tags(html_review),
                                    "pos_review": Transformer.extract_pos_review_body(html_review),
                                    "neg_review": Transformer.extract_neg_review_body(html_review)})

        return hotel

    @staticmethod
    def transform_hotels(raw_hotels_list):
        """Extracting data from raw HTML.

        Args:
            raw_hotels_list: list of HTML content with Hotels data.

        Returns:
            Hotels list.

        """
        hotels = {}

        for raw_hotel in raw_hotels_list:
            hotels[Transformer.extract_hotel_name(raw_hotel)] = Transformer.extract_hotel_link(raw_hotel)
        return hotels

    @staticmethod
    def extract_hotel_name(raw_hotel):
        """Extracting data from raw HTML.

        Args:
            raw_hotel (object): HTML content with Hotel data.

        Returns:
            Hotel name.

        """
        return raw_hotel.find("span", {"class": "sr-hotel__name "}).get_text(strip=True)

    @staticmethod
    def extract_hotel_link(raw_hotel):
        """Extracting data from raw HTML.

        Args:
            raw_hotel (object): HTML content with Hotel data.

        Returns:
            Hotel ref link if exist, if not empty string.

        """
        if raw_hotel:
            return raw_hotel['href']
        else:
            return ""

    @staticmethod
    def extract_date(hml_review):
        """Extracting date from raw HTML.

        Args:
            hml_review (object): HTML content with Review data.

        Returns:
            Review data.

        """
        date_raw = hml_review.find("p", {"class": "review_item_date"}).get_text(strip=True)
        date = datetime.strptime(date_raw, 'Reviewed: %d %B %Y')
        return date

    @staticmethod
    def extract_name(hml_review):
        """Extracting name from raw HTML.

        Args:
            hml_review (object): HTML content with Review data.

        Returns:
            Review user name.

        """
        name = hml_review.find("p", {"class": "reviewer_name"}).get_text(strip=True)
        return name

    @staticmethod
    def extract_country(hml_review):
        """Extracting country from raw HTML.

        Args:
            hml_review (object): HTML content with Review data.

        Returns:
            Review user country.

        """
        country_part = hml_review.find("span", {"class": "reviewer_country"})
        country = country_part.find("span", {"itemprop": "name"}).get_text(strip=True)
        return country

    @staticmethod
    def extract_user_age_group(hml_review):
        """Extracting age group from raw HTML.

        Args:
            hml_review (object): HTML content with Review data.

        Returns:
            Review user age group.

        """
        age_group = hml_review.find("div", {"class": "user_age_group"}).get_text(strip=True)
        return age_group
        
    @staticmethod
    def extract_review_count(hml_review):
        """Extracting review count from raw HTML.

        Args:
            hml_review (object): HTML content with Review data.

        Returns:
            Review user review count.

        """
        review_count = hml_review.find("div", {"class": "review_item_user_review_count"}).get_text(strip=True)
        numbers = [int(count) for count in review_count.split() if count.isdigit()]
        return numbers[0]

    @staticmethod
    def extract_score(hml_review):
        """Extracting review score from raw HTML.

        Args:
            hml_review (object): HTML content with Review data.

        Returns:
            Review user review score.

        """
        score = hml_review.find("span", {"class": "review-score-badge"}).get_text(strip=True)
        return float(score)

    @staticmethod
    def extract_info_tags(hml_review):
        """Extracting info tags from raw HTML.

        Args:
            hml_review (object): HTML content with Review data.

        Returns:
            Review item info tags.

        """

        info_tags_data = hml_review.findAll("li", {"class": "review_info_tag "})

        info_tags_list = [tag.get_text(strip=True) for tag in info_tags_data]

        info_tags = "".join(info_tags_list)

        return info_tags
        
    @staticmethod
    def extract_header(hml_review):
        """Extracting review header from raw HTML.

        Args:
            hml_review (object): HTML content with Review data.

        Returns:
            Review header.

        """
        header_part = hml_review.find("div", {"class": "review_item_header_content "})
        header = header_part.find("span", {"itemprop": "name"}).get_text(strip=True)
        return header

    @staticmethod
    def extract_neg_review_body(hml_review):
        """Extracting review negative opinion from raw HTML.

        Args:
            hml_review (object): HTML content with Review data.

        Returns:
            Review user negative opinion.

        """
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
        """Extracting review positive opinion from raw HTML.

        Args:
            hml_review (object): HTML content with Review data.

        Returns:
            Review user positive opinion.

        """
        pos_body = None
        pos_body_text = None

        review_pos = hml_review.find("p", {"class": "review_pos "})
        if review_pos is not None:
            pos_body = review_pos.find("span", {"itemprop": "reviewBody"})
        if pos_body is not None:
            pos_body_text=pos_body.get_text(strip=True)
        return pos_body_text



