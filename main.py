from bs4 import BeautifulSoup
from pathlib import Path
import io, json, sys, re


def set_author_fullname(soup: BeautifulSoup) -> str:
    callbacks = {
        'lastname': lambda x: soup.find(x).text if soup.find(x) else '',
        'firstname': lambda x: soup.find(x).text if soup.find(x) else '',
        'secondname': lambda x: soup.find(x).text if soup.find(x) else '',
    }
    return ' '.join([callback(key) for key, callback in callbacks.items()])


def parse(dir_path: str, json_path: str) -> None:
    data = {}
    files = Path(dir_path).glob('*')

    for file in files:
        f = io.open(file, mode='r', encoding='utf-8').read()
        soup = BeautifulSoup(f, 'lxml')

        name = soup.find('name').text if soup.find('name') else set_author_fullname(soup)
        links = soup.find('links').text.replace('\n', ' ').strip().split(' ')

        data[name] = [link for link in links if re.search('author_profile', link)][0]

    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    dir_path = 'xml' if len(sys.argv) == 1 else sys.argv[1]
    json_path = 'articles.json' if len(sys.argv) != 3 else sys.argv[2]

    parse(dir_path, json_path)
