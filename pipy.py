import sys

__author__ = 'Loiso'
from xml.etree import ElementTree
from urllib.request import urlopen
import httplib2
import json
import csv
import sys


def get_distributions(simple_index='https://pypi.python.org/simple/'):
    with urlopen(simple_index) as f:
        tree = ElementTree.parse(f)
    return [a.text for a in tree.iter('a')]


def scrape_links(dist, simple_index='https://pypi.python.org/simple/'):
    with urlopen(simple_index + dist + '/') as f:
        tree = ElementTree.parse(f)
    return [a.attrib['href'] for a in tree.iter('a')]


def get_packagedescription(name):
    h = httplib2.Http()
    url = "http://pypi.python.org/pypi/%s/json" % name
    (resp_headers, content) = h.request(url, "GET")
    data = json.loads(content.decode("utf-8", "ignore"))
    return data


def main():
    with open('eggs.csv', 'w', newline='', encoding='utf-8') as csvfile:
        f = csv.writer(csvfile)
        a = get_distributions()
        for b in a:
            g = get_packagedescription(b)
            l = g.get('info')
            l.update(l.pop('downloads'))
            f.writerow(list(l.values()))
        return 0


if __name__ == '__main__':
    sys.exit(main())
