from requests import Session

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip,deflate, br',
    'Accept-Language': 'ru,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '7948',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '_ym_uid=1654432160110788019; SCookieGUID=195CCC22%2D6199%2D44F3%2DA68D%2DF483F787CDE3; SUserID=539967278; _ym_d=1690010399; _ym_isad=1; __utmc=216042306; __utma=216042306.1924992643.1686053082.1690010399.1690014730.8; __utmz=216042306.1690014730.8.4.utmcsr=yandex|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=216042306.3.10.1690014730',
    'Host': 'elibrary.ru',
    'Origin': 'https://elibrary.ru',
    'Referer': 'https://elibrary.ru/authors.asp',
    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.0.2526 Yowser/2.5 Safari/537.36'
}

data = {
    'authors_all': '',
    'pagenum': '',
    'authorbox_name': '',
    'selid': '',
    'orgid': '916',
    'orgadminid': '',
    'surname': '',
    'codetype': 'SPIN',
    'codevalue': '',
    'town': '',
    'countryid': '',
    'orgname': 'Томский государственный педагогический университет',
    'rubriccode': '',
    'metrics': '1',
    'sortorder': '0',
    'order': '0',
}
work = Session()

response = work.post("https://elibrary.ru/authors.asp", headers=headers, data=data, allow_redirects=True)
