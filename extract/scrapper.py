"""Scrapping (or extracting) HTML module in Python.

This module implements 'extract' functionality, in this particular case it is
extracting reviews from hotels in www.booking.com page. Mainly Selenium web drive is in use.

.. Introduction to web scrapping:
   https://realpython.com/python-web-scraping-practical-introduction/
"""

from selenium import webdriver
import re
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from webdriverdownloader import GeckoDriverDownloader
from bs4 import BeautifulSoup
import os


def get_driver_path():
    """Reconstructs correct path to Firefox driver.

    Note:
        Because GeckoDriverDownloader has been used for driver download,
        then GeckoDriverDownloader is also use for determine path to driver
    """

    firefox_downloader = GeckoDriverDownloader()
    return firefox_downloader.get_download_path() + '\\' + os.listdir(firefox_downloader.get_download_path())[
        0] + '\\' + firefox_downloader.get_driver_filename()


def force_english_version(driver):
    """Makes site source coherently in english.
    """

    try:
        language = driver.find_element_by_class_name('lang_en-gb')
        eng_site = language.find_element_by_class_name('no_target_blank ').get_attribute("href")
    except NoSuchElementException as e:
        print(e)
        return

    driver.get(eng_site)


def get_driver():
    """Returns web Firefox driver created in headless mode (no visible browser).
    """
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    # 1 - Allow all images
    # 2 - Block all images
    # 3 - Block 3rd party images
    profile.set_preference("permissions.default.image", 2)

    try:
        return webdriver.Firefox(executable_path=get_driver_path(), options=options, firefox_profile=profile)
    except WebDriverException as e:
        print(e)
        return None


def collect_reviews(driver, review_list):
    """Attach all reviews present on one page(also archived).

    Args:
        driver: The web driver which gives ability to search in web content.
        review_list: List of partial search results, function extends this list with new results.
    """

    content = BeautifulSoup(driver.page_source, 'lxml')
    review_list.extend(content.findAll("li", {"class": "review_item clearfix "}))
    review_list.extend(content.findAll("li", {"class": "review_item clearfix archive_item "}))


def collect_hotels(driver, hotel_list):
    """Collect all hotels from given HTML page.

    Args:
        driver: the web driver which gives ability to search in web content.
        hotel_list: list of partial search results, function extends this list with new results.
    """

    content = BeautifulSoup(driver.page_source, 'lxml')
    hotel_item = content.find("a", {"class": "hotel_name_link url"})
    if hotel_item:
        hotel_list.append(hotel_item)

    if hotel_item:
        for i in range(9):
            hotel_item = hotel_item.find_next("a", {"class": "hotel_name_link url"})
            if hotel_item:
                hotel_list.append(hotel_item)
            else:
                break


def get_hotels_from_city(city):
    """Colect all hotels from given city name.

    Args:
        city (str): the web driver which gives ability to search in web content.

    Returns:
        Only 10 hotels' list are returned. Content of this list is hotels data in HTML format.
    """

    driver = get_driver()

    driver.get("http://www.booking.com")

    force_english_version(driver)

    try:
        city_search = driver.find_element_by_id('ss')
        city_search.click()
        city_search.clear()
        city_search.send_keys(city)
        driver.find_element_by_class_name("sb-searchbox__button  ").click()
    except NoSuchElementException as e:
        print(e)
        return
    hotels_list = []
    collect_hotels(driver, hotels_list)

    driver.close()
    return hotels_list[:10]


def get_hotel_address(driver):

    address = None
    try:
        address = driver.find_element_by_class_name("hotel_address")
    except NoSuchElementException as e:
        print(e)

    return address.text if address is not None else ''


def make_hotel_review_url(hotel_href):

    result_stage_one = re.split("/hotel/[a-z]*/", hotel_href)

    hotel_loc_part = re.search("/hotel/[a-z]*/", hotel_href)

    return hotel_loc_part.group(0).replace("/hotel/", "/reviews/") + "hotel/" + result_stage_one[1];


def scrap(url):
    """Main scrapping function, in general this function collects and returns all reviews from all pages.
    For navigation between pages "review_next_page_link" button is used.

    Args:
        url (str): the url address to hotel page.

    Returns:
        List of reviews in HTML format.
    """
    driver = get_driver()

    driver.get(url)

    review_list = []
    collect_reviews(driver, review_list)

    while True:
        try:
            driver.find_element_by_id("review_next_page_link").click()
        except NoSuchElementException:
            break
        collect_reviews(driver, review_list)

    hotel_address = get_hotel_address(driver)

    driver.quit()

    return review_list, hotel_address
