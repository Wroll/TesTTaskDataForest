# import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
# from requests_html import HTMLSession
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import xlsxwriter

driver = webdriver.Chrome("D:\\drosel\\Driver\\chromedriver.exe")
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()
row = 0


def write_into_excel_document(title, category, location, website, row):
    worksheet.write(row, 0, title)
    worksheet.write(row, 1, category)
    worksheet.write(row, 2, location)
    worksheet.write(row, 3, website)


def get_amount_of_pages(url):
    driver.get(url)
    try:
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'button.pagination-button')))
    except TimeoutException:
        print("element not presented")
        raise
    elements = driver.find_elements_by_css_selector('button.pagination-button')
    return max([int(element.text) for element in elements if element.text.isdigit()])


def pull_all_links(url):
    driver.get(url)
    try:
        time.sleep(5)
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//html/body/main/section[3]/div[2]/div[3]/div[last()]')))
    except TimeoutException:
        print('element not presented')
        raise
    links = driver.find_elements_by_css_selector('div article a.lazypreload.lazyloaded')
    result = [link.get_attribute("href") for link in links]
    print("------------------------------")
    print(result)
    print(f"Amount of links in {url} is {len(result)}")
    print("------------------------------")
    return result


def get_info(links):
    global row
    for link in links:
        driver.get(link)
        title = driver.find_element_by_css_selector('div.block.heading.prose.text-left h1').text
        category = driver.find_element_by_css_selector(
            'ul.quick-details li:first-child div.quick-details-content span:last-child').text
        location = driver.find_element_by_css_selector(
            'ul.quick-details li:last-child div.quick-details-content span:last-child').text
        website = driver.find_element_by_css_selector('div.block.activity-buttons div:last-child a').get_attribute(
            'href')
        write_into_excel_document(title, category, location, website, row)
        row += 1
        result = (title, category, location, website)
        print(result)


def parse(regions):
    for region in regions:  # amount of url's
        for p in range(1, get_amount_of_pages(region) + 1):
            start = time.time()
            all_links_from_page = pull_all_links(f"{region + str(p)}")
            get_info(all_links_from_page)
            print(time.time() - start)


if __name__ == '__main__':
    URLS = ["https://iwilltravelagain.com/canada/?page=", 'https://iwilltravelagain.com/usa/?page=',
            "https://iwilltravelagain.com/europe/?page=", 'https://iwilltravelagain.com/latin-america-caribbean/?page=',
            'https://iwilltravelagain.com/australia-new-zealand-asia/?page=']
    try:
        # driver.delete_all_cookies()
        parse(URLS)
    finally:
        driver.quit()
        workbook.close()
