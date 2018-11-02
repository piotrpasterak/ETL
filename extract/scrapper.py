from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from webdriverdownloader import ChromeDriverDownloader
from bs4 import BeautifulSoup
import os


def get_driver_path():
    """
    get_driver_path - this function reconstruct correct path to Chrome driver.
    Because ChromeDriverDownloader has been used for driver download,
    then ChromeDriverDownloader is also use for determine path to driver
    """

    chrome_downloader = ChromeDriverDownloader()
    return chrome_downloader.get_download_path() + '\\' + os.listdir(chrome_downloader.get_download_path())[
        0] + '\\' + chrome_downloader.get_driver_filename()


def get_driver():
    """
    get_driver - This function return web Chrome driver created in headless mode (no visible browser)
    """
    options = Options()
    options.add_argument("headless")

    try:
        return webdriver.Chrome(executable_path=get_driver_path(), options=options)
    except WebDriverException as e:
        print(e)
        return None


def collect_reviews(driver, review_list):
    """
    collect_reviews - this function search and returns all reviews on one page(also archive)
    """
    content = BeautifulSoup(driver.page_source, 'lxml')
    review_list.append(content.findAll("li", {"class": "review_item clearfix "}))
    review_list.append(content.findAll("li", {"class": "review_item clearfix archive_item "}))


def scrap(url):
    """
    scrap - main scrapping function, in general this function collects and returns all reviews from all pages.
    For navigation between pages "review_next_page_link" button is used.
    """
    driver = get_driver()
    driver.get(url)

    review_list = []
    collect_reviews(driver, review_list)

    while True:
        try:
            button = driver.find_element_by_id("review_next_page_link")
        except NoSuchElementException:
            break
        button.click()
        collect_reviews(driver, review_list)

    driver.quit()

    return review_list


if __name__ == '__main__':
    """
    main function for web scrapper, just result of scrapping wil be displayed. )
    Please note that Chrome Web browser is required to be present in system! 
    """
    print(scrap("http://www.booking.com/reviews/pl/hotel/cracowdayskrakow.html"))
