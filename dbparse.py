from bs4 import BeautifulSoup
from pathlib import Path
from config import host, user, password, db_name
import io, json, sys, re, mariadb

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


# cur.execute("SELECT first_name,last_name FROM tspu_staff")
#
# for (first_name, last_name) in cur:
#     print(f"First Name: {first_name}, Last Name: {last_name}")

# cur.execute(
#     "INSERT INTO tspu_staff (first_name, last_name, crd_id, Expr1, gph, elibrary, web_of_science, scopus, orcid, google_scholar_citations) VALUES (?, ?, 3555, 5, 3, 'aaa', 'aaa', 3, 5, 1)",
#     (name, fam))
# conn.commit()

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

        # try:
        #     cur.execute(
        #         """INSERT INTO tspu_staff (last_name, first_name, middle_name, elibrary, orcid, scopus, Expr1, web_of_science,
        #          crd_id, google_scholar_citations, gph, id)
        #         VALUES (?, ?, ?, ?, 1, 2, 3, 4, 5555, 6, 7, 1957)
        #         on duplicate KEY update last_name = 'Повторение' """,
        #         (db_ins)
        #     )
        #     conn.commit()
        #     print('Добавлено')
        # except Exception as e:
        #     print(f'Ошибка добавления {e}')
        # counter += 1
        # if counter >= 1:
        #     break

        cur.execute(
            "SELECT last_name, first_name, middle_name FROM tspu_staff WHERE last_name = ? and first_name = ? and middle_name = ?",
            (names)
            )

        for (last_name, first_name, middle_name) in cur:
            if last_name == names[0] and first_name == names[1] and middle_name == names[2]:
                cur.execute(
                    """UPDATE tspu_staff SET elibrary = ? WHERE last_name = ? and first_name = ? and middle_name = ?""",
                    (db_ins)
                    )
                conn.commit()
                print('Обновил')
                break


if __name__ == '__main__':
    dir_path = 'xml' if len(sys.argv) == 1 else sys.argv[1]

    parse(dir_path)
