import elib_parse as elib
import mariadb
import sys


def update(background_mode: bool = False, user: str = "root", password: str = "root", host: str = "localhost",
           db_name: str = "mydb"):
    """Исполняющая функция, запускающая сбор данных с библиотеки и последующее обновление базы данных"""
    elib.get_all_links(background_mode)

    # Подключение к БД
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

    # Получение курсора
    cur = conn.cursor()

    for emp_num in range(len(elib.names)):
        name = elib.names[emp_num].strip()
        link = [elib.profile_links[emp_num]]
        names = name.split('  ')

        if len(names) == 4:
            del names[1]
        if len(names) == 2:
            names.append('')

        db_ins = link + names

        if len(db_ins) == 4:
            cur.execute(
                """UPDATE tspu_staff SET elibrary = ? WHERE last_name = ? and first_name = ? and middle_name = ?""",
                db_ins
            )
        conn.commit()

    print('Обновление прошло успешно')


update(True)
