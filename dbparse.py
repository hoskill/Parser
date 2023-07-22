from bs4 import BeautifulSoup
from pathlib import Path
from config import host, user, password, db_name
import io, sys, re, mariadb

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        port=3306,
        database=db_name
    )
    print('Подключено')
except mariadb.Error as e:
    print(f"Ошибка подключения: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


def set_author_fullname(soup: BeautifulSoup) -> str:
    callbacks = {
        'lastname': lambda x: soup.find(x).text if soup.find(x) else '',
        'firstname': lambda x: soup.find(x).text if soup.find(x) else '',
        'secondname': lambda x: soup.find(x).text if soup.find(x) else ''
    }
    return ' '.join([callback(key) for key, callback in callbacks.items()])


def parse(dir_path: str) -> None:
    files = Path(dir_path).glob('*')

    for file in files:
        f = io.open(file, mode='r', encoding='utf-8').read()
        soup = BeautifulSoup(f, 'lxml')

        name = soup.find('name').text if soup.find('name') else set_author_fullname(soup)
        links = soup.find('links').text.replace('\n', ' ').strip().split(' ')
        names = name.split(' ')
        link = [[link for link in links if re.search('author_profile', link)][0]]
        db_ins = link + names

        cur.execute(
            """UPDATE tspu_staff SET elibrary = ? WHERE last_name = ? and first_name = ? and middle_name = ?""",
            (db_ins)
        )
        conn.commit()

    print('Обновление прошло успешно')


if __name__ == '__main__':
    dir_path = 'xml' if len(sys.argv) == 1 else sys.argv[1]

    parse(dir_path)
