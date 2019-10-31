import os
import json
from apiclient.bizon365 import Webinars

API_KEY = os.getenv('API_KEY', None)

bizon = Webinars(api_key=API_KEY)

# subpages = bizon.get_subpages()
# print('List of all subpages is: \n {}'.format(subpages))
#
# reports = bizon.get_list(live=0, auto=1)
# print('List of all reports is:')
# print(json.dumps(reports, indent=4, sort_keys=True))

# webinar_report = bizon.get_webinar_report('XXXXX')
# print(json.dumps(webinar_report, indent=4, sort_keys=True))

webinar_report = bizon.get_webinar_viewers('XXXX')
print(json.dumps(webinar_report, indent=4, sort_keys=True))