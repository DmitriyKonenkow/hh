import httplib2
import json
from pprint import pprint
__author__ = 'Loiso'

h = httplib2.Http()
(resp_headers, content) = h.request("https://pypi.python.org/simple/", "GET")
data = json.loads(content.decode("utf-8"))

pprint(data)