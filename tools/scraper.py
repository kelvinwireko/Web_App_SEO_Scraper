import time
import os, sys

from bs4 import BeautifulSoup as Soup
import people_also_ask as paa
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium_recaptcha import Recaptcha_Solver
import streamlit as st
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


# Get URL from HTML tags and save to a python dictionary
serp_titles_url = {"title": [], "url": []}


def get_driver():
    firefox_binary = FirefoxBinary('/usr/bin/firefox/')
    options = Options()
    options.headless = True
    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options, firefox_binary=firefox_binary)


def page_source(keyword):
    driver = get_driver()
    url = f"https://google.com/search?&gl=us&q={keyword}"
    driver.get(url)
    page_source = driver.page_source
    soup = Soup(page_source, "lxml")
    driver.quit()
    return soup


def scrape_serp_results(soup):
    """
    Get the title and url of the first 10 results on Google search.
    :param soup:
    :param keyword:
    :return:
    """
    # Find first 10 results on Google and get html tag containing URL
    for r in soup.select('#search div.yuRUbf'):
        for div in r:
            titles = div.select("h3")
            serp_titles_url["url"].append(str(div.get('href')))
            if len(titles) >= 1:
                h3 = titles[0]
                serp_titles_url["title"].append(h3.get_text())
    for j in serp_titles_url["url"]:
        if j == "None":
            serp_titles_url["url"].remove(j)
    time.sleep(3)
    return serp_titles_url


def search_related_results(soup):
    # Find and store search related results in a list
    arr = []
    for related_results in soup.select("#search div.EIaa9b"):
        for results in related_results:
            result = related_results.select("a")
            for i in result:
                arr.append(i.get_text())
    # Remove duplicates from list and save as a new list
    search_rela_results = [arr[i] for i in range(len(arr)) if i == arr.index(arr[i])]
    return search_rela_results


def scrape_headings(url=serp_titles_url["url"]):
    """
    This function gets the heading tags of a page when targeting keyword
    :return:
    """
    driver = get_driver()

    article_headings = []
    for i in url:
        driver.get(i)
        page_source = driver.page_source
        soup = Soup(page_source, 'lxml')
        heading_tags = ["h1", "h2", "h3", "h4"]
        for j in soup.findAll(heading_tags):
            article_headings.append(f"{j.name.capitalize()}: {j.text.strip().title()}\n")
        time.sleep(2)
    return article_headings


def scrape_paa(keyword):
    questions = paa.get_related_questions(keyword, 10)
    return questions


if __name__ == "__main__":
    results = search_related_results("gecko")
    print(results)
