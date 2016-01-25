import lxml.html as html

html_file = "tmp.html"

file = open(html_file, 'r', encoding='utf-8')
temp_string = file.read()
file.close()
page = html.parse(temp_string)
page
print(temp_string)