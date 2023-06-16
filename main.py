import json

from bs4 import BeautifulSoup
from pathlib import Path
import io

names = []
links = []
data = {}

directory = 'xml'
files = Path(directory).glob('*')
for file in files:
    f = io.open(file, mode='r', encoding='utf-8').read()
    soup = BeautifulSoup(f, 'lxml')

    name = soup.find('name')
# print(name.text.strip())
    names.append(name.text)

    link = soup.find('links').text.replace('\n', ' ').strip().split(' ')
    del link[0]
# print(link.text.strip())
    links.append(*link)

print(names)
print(links)
for i in range(len(names)):
    data[names[i]] = links[i]

with open('articles.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
