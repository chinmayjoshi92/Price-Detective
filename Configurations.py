import requests
from Database import *
from googlesearch import search
from bs4 import BeautifulSoup
from datetime import datetime
import xlwt


def search_on_google(query, no_of_results=1):
    """
    Search the given query on google. It'll give top result.
    :param no_of_results: Number of results to get from search.
    :param query: product to be searched.
    :return: result
    """
    for result in search(query, num=5, stop=no_of_results, pause=1.5):
        return result


def send_get_request(site_url):
    """
    Send GET request to the site url which is passed as an argument
    :param site_url: url to which GET request to be send
    :return: response from the GET request. if any exception returns a list containing
             False in index 0 and cause of exception at index 1.
    """
    for attempt in range(0, 10):
        try:
            ret = requests.get(site_url)
            break
        except requests.exceptions.RequestException as e:
            ret = [False, e]

    return ret


def find_price(html_text, section, sect_attri):
    """
    Find price from return content
    :param html_text: received text
    :param section: Ection from price to be search
    :param sect_attri: search attribute
    :return: price
    """
    soup = BeautifulSoup(html_text, features="html.parser")

    """
    THIS CODE CAN BE FURTHER EXTENTED.....
    tags = soup('span')
    for tag in tags:
        print(tag.contents)
        if not tag.contents:
            continue
        for line in tag.contents:
            if "price" in line:
                print(line)
                break
    line = ""
    """

    price = soup.find(section, attrs=sect_attri)
    return price
