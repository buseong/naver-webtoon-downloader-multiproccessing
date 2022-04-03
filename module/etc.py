import urllib.request
from bs4 import BeautifulSoup


def sort_num(arag, numer):
    k = len(arag) // numer
    el = len(arag) % numer
    arr = [[], ]
    count = 0
    last = 1
    for ch_nam in range(k * numer):
        if ch_nam == (k * last):
            arr.append([], )
            count += 1
            last += 1
        arr[count].append(arag[ch_nam])
    for el_ch in range(el):
        k = len(arag) - el_ch - 1
        arr[numer - 1].append(arag[k])
    return arr


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
