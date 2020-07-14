import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import csv
import time

URL = "https://iwilltravelagain.com"


def write_csv(data):
    with open('data.csv', 'a', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow((data['title'], data['category'], data['location'], data['link']))


def get_response():
    response = requests.get(
        'https://iwilltravelagain.com/wp-json/FH/activities?post_id=143&key=rows_3_grid_activities',
        params={'post_id': '143', 'key': 'rows_3_grid_activities'},
        headers={'Content-Type': 'application/json; charset=UTF-8', 'Strict-Transport-Security': 'max-age=15552000',
                 'Expect-CT': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"',
                 'cf-request-id': '03eaa4d1b90000f2cc861c1200000001', 'Cache-Control': 'public, max-age=43200',
                 'Link': '<https://iwilltravelagain.com/wp-json/>; rel="https://api.w.org/"'},
    )
    return response.json()


def get_links():
    links = []
    data_from_external_api = get_response()
    for object in data_from_external_api:
        links.append(data_from_external_api[object]['link'])
    return links


def parse(partial_link):
    r = requests.get(f"{URL + partial_link}")
    soup = BeautifulSoup(r.text, 'html.parser')
    link = soup.find(alt="Click here to Visit Website", href=True)['href']
    title = soup.find('h1').get_text()
    category = soup.find(class_="quick-details-content").findChildren()[-1].get_text()
    location = soup.find(class_="quick-details").findChildren()[-1].get_text()
    data = {'title': title, 'category': category, 'location': location, 'link': link}
    write_csv(data)
    print(f"Title: {title}, Category: {category}, Location: {location}, Link: {link} ")


def main():
    links = get_links()
    with Pool(60) as p:
        p.map(parse, links)


if __name__ == '__main__':
    try:
        start = time.time()
        main()
    finally:
        print(time.time() - start)