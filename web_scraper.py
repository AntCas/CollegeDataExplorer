import requests
import pprint
import json
from bs4 import BeautifulSoup
import re
import csv

pp = pprint.PrettyPrinter(indent=2, depth=8)

root_url = 'https://www.usnews.com/best-colleges/rankings/national-universities/data'

# Allow debugging of HTTP headers
#from debug_requests import DebugRequests as dr
#debug = dr()
#debug.debug_requests_on()

# Change the User-Agent in the HTTP request header to one which isn't blocked by
# usnews.com (The User Agent "python-requests" is blocked by usnew.com).
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    'Accept-Encoding': ', '.join(('gzip', 'deflate')),
    'Accept': '*/*',
    'Connection': 'keep-alive',
}

# download the first page of data
next_url = "%s?_page=1&format=json" % (root_url)
r = requests.get(next_url, headers=headers)
print next_url

# The json for page one can't be grabbed by itself so it has to be extracted
# from the webpage before it can be processed. The json data is processed by
# extracting the university rankings data from the rest of the json data.
soup = BeautifulSoup(r.text)
page_one_json = json.loads(soup.find_all('script', {"data-for": "search-application"})[0].text)
university_info_json = page_one_json['model']['results']['data']['items']

# The rest of the json data can be dowloaded directly as json. This data shows
# up on usnews.com in an "infinite scroll" style. Here we're continually
# requesting the next page of info manually until we hit a 404 (page not found).
page_num = 2
while r.status_code == "200":
    next_url = "%s?_page=%d&format=json" % (root_url, page_num)
    r = requests.get(next_url, headers=headers)
    university_info_json += json.loads(r.text)['data']['results']['data']['items']
    print next_url
    page_num += 1

# Save the json data
with open('USNewsNationalUniversities.json', 'w') as output_file:
    json.dump(university_info_json, output_file)
