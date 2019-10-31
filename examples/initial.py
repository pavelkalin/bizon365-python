import os
import json
from apiclient.bizon365 import Webinars

API_KEY = os.getenv('API_KEY', None)

bizon = Webinars(api_key=API_KEY)

subpages = bizon.get_subpages()
print('List of all subpages is: \n {}'.format(subpages))
