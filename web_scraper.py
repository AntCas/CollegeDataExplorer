import requests
import pprint
import json
from bs4 import BeautifulSoup

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
soup = BeautifulSoup(r.text, "html5lib")
json_string = soup.find('script', {"data-for": "search-application"}).text
page_one_data = json.loads(json_string)
university_info = page_one_data['model']['results']['data']['items']

# The rest of the json data can be dowloaded directly as json. This data shows
# up on usnews.com in an "infinite scroll" style. Here we're continually
# requesting the next page of info manually until we hit a 404 (page not found).
page_num = 2
while True:
    next_url = "%s?_page=%d&format=json" % (root_url, page_num)
    r = requests.get(next_url, headers=headers)
    print next_url

    if r.status_code != 200:
        print "Got a %d status code" % r.status_code
        break

    university_info += json.loads(r.text)['data']['results']['data']['items']
    page_num += 1


print "# pages scraped = %d" % (page_num - 1)

# Save the json data
with open('college_data.json', 'w') as output_file:
    json.dump(university_info, output_file)
