import urllib.request
from bs4 import BeautifulSoup


def get_all_wt():
    url_arr = []
    html = urllib.request.urlopen('https://comic.naver.com/webtoon/weekday')
    Soup = BeautifulSoup(html.read(), "html.parser")
    html.close()
    get_url = Soup.select('a')
    for get_url in get_url:
        j = get_url['href']
        i = "https://comic.naver.com" + str(j)
        if 'weekday=' and 'list?' in i:
            if len(i) == 63:
                if i in url_arr:
                    pass
                else:
                    url_arr.append(i)

    return url_arr

