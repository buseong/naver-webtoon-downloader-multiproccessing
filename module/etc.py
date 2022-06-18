import urllib.request
from bs4 import BeautifulSoup


def get_id_wk(url):

    if 'no' in url:
        url = url
        ider = url[47:53]
        weekday = url[68:]
        adap = "https://comic.naver.com/webtoon/list?titleId=" + str(ider) + "&weekday=" + str(weekday)
    else:
        ider = url[45:51]
        weekday = url[60:]
        adap = url

    return adap, ider, weekday


def get_soup(url):

    html = urllib.request.urlopen(url)
    Soup = BeautifulSoup(html.read(), "html.parser")
    html.close()

    return Soup
