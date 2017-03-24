import json
import csv
import pprint

pp = pprint.PrettyPrinter(indent=2, depth=8)

with open('college_data.json', 'r') as j:
    json_data = json.loads(j.read())

#pp.pprint(json_data)

with open('college_data.csv', 'w') as c:
    csv_file = csv.writer(c)
    for data in json_data:
        csv_file.writerow([data['institution']['displayName'],
              data['ranking']['displayRank'],
              data['searchData']['acceptance-rate']['rawValue']])
