from html.parser import HTMLParser


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()

if __name__ == '__main__':
    html = '<a href="#">Demo <em>(&not; \u0394&#x03b7;&#956;&#x03CE;)</em></a>'
    print(strip_tags(html))