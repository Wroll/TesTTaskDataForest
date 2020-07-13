import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
# import xlsxwriter

url = "https://iwilltravelagain.com"
# row = 0
# workbook = xlsxwriter.Workbook('data1.xlsx')
# worksheet = workbook.add_worksheet()
#
#
# def write_into_excel_document(title, category, location, website, row):
#     worksheet.write(row, 0, title)
#     worksheet.write(row, 1, category)
#     worksheet.write(row, 2, location)
#     worksheet.write(row, 3, website)


def get_links():
    links = []
    response = requests.get(
        'https://iwilltravelagain.com/wp-json/FH/activities?post_id=143&key=rows_3_grid_activities',
        params={'post_id': '143', 'key': 'rows_3_grid_activities'},
        headers={'Content-Type': 'application/json; charset=UTF-8', 'Strict-Transport-Security': 'max-age=15552000',
                 'Expect-CT': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"',
                 'cf-request-id': '03eaa4d1b90000f2cc861c1200000001', 'Cache-Control': 'public, max-age=43200',
                 'Link': '<https://iwilltravelagain.com/wp-json/>; rel="https://api.w.org/"'},

    )
    json_response = response.json()
    for l in json_response:
        links.append(json_response[l]['link'])
    h = links[:10]
    return h


def parse(partial_link):
    global row
    r = requests.get(f"{url + partial_link}")
    soup = BeautifulSoup(r.text, 'html.parser')
    link = soup.find(alt="Click here to Visit Website", href=True)['href']
    title = soup.find('h1').get_text()
    category = soup.find(class_="quick-details-content").findChildren()[-1].get_text()
    location = soup.find(class_="quick-details").findChildren()[-1].get_text()
    # write_into_excel_document(title, category, location, link, row)
    row += 1
    print(f"Title: {title}, Category: {category}, Location: {location}, Link: {link} ")


# TODO make a function to write results
def main():
    links = get_links()
    with Pool(1) as p:
        p.map(parse, links)


if __name__ == '__main__':
    try:
        # main()
        parse(get_links())
    finally:
        pass
        # workbook.close()
