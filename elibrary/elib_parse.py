from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

profile_links = []
names = []
error_description: str = 'Произошла ошибка при подключении к сервису...'


def lib_connect(background_mode: bool = False) -> None:
    """Выбор режима работы браузера и подключение к библиотеке
    Для перевода браузера в фоновый режим передайте 0 """

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    if not background_mode:
        options.add_argument("--headless=new")
        print('Браузер работает в фоновом режиме...')
    else:
        print('Браузер работает в обычном режиме...')

    global driver
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://elibrary.ru/authors.asp")
        print("Подключено...")
    except Exception as e:
        print(f'Произошла ошибка при подключении... {e}')
        driver.close()
        driver.quit()


def get_employee(university: str = "ТГПУ", town: str = "Томск") -> None:
    """Выбор учебного заведения и получение списка преподавателей
    По умолчанию: университет - ТГПУ, город - Томск"""

    try:
        driver.implicitly_wait(20)
        choose_button = driver.find_element(By.XPATH, '//*[@id="show_param"]/table[3]/tbody/tr[2]/td[2]/div')
        choose_button.click()
        driver.switch_to.frame("fancybox-frame")

        org_name = driver.find_element(By.CSS_SELECTOR, '#qwd')
        org_name.click()
        org_name.send_keys(university)
        print('Учебное заведение выбрано...')

        cities = driver.find_element(By.XPATH, '//*[@id="town"]')
        cities.click()
        cities.send_keys(town)
        cities.send_keys(Keys.ENTER)
        print('Город выбран...')

        driver.implicitly_wait(10)
        org_button = driver.find_element(By.XPATH, '/html/body/center/form/table[2]/tbody/tr/td[2]/a')
        org_button.click()
        print('Организация найдена...')

        driver.switch_to.default_content()

        search_button = driver.find_element(By.CSS_SELECTOR, ".butred:last-child")
        search_button.click()
        print('Список сотрудников получен...')

    except Exception as e:
        print(f'Произошла ошибка при получении сотрудников... {e}')
        driver.close()
        driver.quit()


def get_data_by_page() -> None:
    """Сбор ссылок и ФИО сотрудников со страницы"""
    try:
        links = driver.find_elements(By.CSS_SELECTOR, 'tr[id]')
        all_names = driver.find_elements(By.CSS_SELECTOR, 'tr [valign="top"] > td[align="left"] > font > b')

        for employee in links:
            link = "https://www.elibrary.ru/author_profile.asp?id=" + employee.get_attribute('id')[1:]
            profile_links.append(link)

        for employee in all_names:
            name = employee.text
            names.append(name)

    except Exception as e:
        print(f'Произошла ошибка во время сбора ссылок... {e}')
        driver.close()
        driver.quit()


def get_all_links(background_mode: bool = False, university: str = "ТГПУ", town: str = "Томск"):
    """Сбор ссылок всех сотрудников из библиотеки"""
    counter: int = 1
    lib_connect(background_mode)
    get_employee(university, town)
    next_page = driver.find_element(By.CSS_SELECTOR, '#pages > table > tbody > tr > td:nth-child(12) > a')
    last_page = driver.find_element(By.CSS_SELECTOR, '#pages > table > tbody > tr > td:nth-child(13) > a')

    # Проверка, что следующая страница не является последней
    while next_page.get_attribute('href') != last_page.get_attribute('href'):
        driver.implicitly_wait(25)
        get_data_by_page()
        print(f'Собрали информацию с {counter} страницы...')
        counter += 1
        next_page.click()
        next_page = driver.find_element(By.CSS_SELECTOR, '#pages > table > tbody > tr > td:nth-child(12) > a')
        last_page = driver.find_element(By.CSS_SELECTOR, '#pages > table > tbody > tr > td:nth-child(13) > a')

    # Получаем ссылки с последней страницы
    get_data_by_page()
    print(f'Информация с {counter} страницы успешно собрана...')
    next_page.click()
    get_data_by_page()

    print('Все ссылки собраны успешно...')

    driver.close()
    driver.quit()
