from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import multiprocessing
import shutil
import numpy as np
import os
url_arr = []
def downloader(ls):
    html = urllib.request.urlopen('https://comic.naver.com/webtoon/weekday')
    Soup = BeautifulSoup(html.read(), "html.parser")
    html.close()
    get_url = Soup.select('a')
    for get_url in get_url:
        i = get_url['href']
        if 'weekday=' and 'list?' in i:
            if len(i) == 40:
                temp = "https://comic.naver.com" + str(i)
                url_arr.append(temp)
    for lanm in ls:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        number = 1
        arr = []
        inputer = url_arr[lanm]
        if 'no' in inputer:
            url = inputer
            id = url[47:53]
            weekday = url[68:]
            adap = "https://comic.naver.com/webtoon/list?titleId=" + str(id) + "&weekday=" + str(weekday)
        else:
            url = inputer
            id = url[45:51]
            weekday = url[60:]
            adap = url
        html = urllib.request.urlopen(adap)
        Soup = BeautifulSoup(html.read(), "html.parser")
        html.close()
        get_url = Soup.select('a')
        get_title = Soup.select('.title')
        eposide_title = str(get_title[0]).lstrip('<span class="title">').rstrip('</span>')
        k = 0
        for get_url in get_url:
            k += 1
            i = get_url['href']
            if k % 2 == 0:
                if 'weekday' in i:
                    if 'no' in i:
                        nu = (i.lstrip(f'/webtoon/detail?titleId={id}').lstrip(r'&no=').rstrip(weekday).rstrip(
                            r'&weekday='))
                        arr.append(int(nu))
        maxValue = np.max(arr)
        brr = []
        for l in range(int(maxValue)):
            edit = "https://comic.naver.com/webtoon/detail?titleId=" + id + "&no=" + str(l+1) + "&weekday=" + weekday
            brr.append(edit)
        la = 1
        basic_file = os.getcwd().replace("\\","/")
        new_img = None
        flod_path = str(id)
        for epsoide in brr:
            print(f'{eposide_title} {la}/{maxValue}화 작업중')
            try:
                os.makedirs(f"{basic_file}/{eposide_title}/{la}")
            except:
                print(f'didnt make {basic_file}/{eposide_title}/{la}')
            try:
                os.mkdir(flod_path)
            except:
                pass
            custom_img = []
            html = urllib.request.urlopen(epsoide)
            Soup = BeautifulSoup(html.read(), "html.parser")
            html.close()
            img_url = Soup.select('img')
            for img_url in img_url:
                j = img_url.get('src')
                if j is None:
                    pass
                elif 'IMAG01' in j:
                    custom_img.append(j)
            num = 0
            img_arr = []
            for image_url in custom_img:
                num += 1
                img_path = basic_file + f"/{flod_path}/" + str(num) + '.jpg'
                urllib.request.urlretrieve(image_url, img_path)
                img_arr.append(img_path)
            number += 1
            for i in range(len(img_arr) - 1):
                if i == 0:
                    first_img = Image.open(img_arr[i])
                else:
                    first_img = new_img
                second_img = Image.open(img_arr[i + 1])
                first_img_size = first_img.size
                second_img_size = second_img.size
                new_img = Image.new('RGB', (first_img_size[0], first_img_size[1] + (second_img_size[1])), (255, 255, 255))
                new_img.paste(first_img, (0, 0))
                new_img.paste(second_img, (0, first_img_size[1]))
            n = 1
            cut_img_y = 0
            img = new_img
            pix = np.array(img)
            num = 0
            for j in range(img.size[1]):
                i = np.arange(0, 690)
                judge = pix[j][i]
                if np.max(judge) == np.min(judge) == 255:
                    num += 1
                elif np.max(judge) == np.min(judge) == 0:
                    num += 1
                if num == 300:
                    cut_img = img.crop((0, cut_img_y, 690, j))
                    if int(cut_img.size[1]) == 300:
                        n = n - 1
                    else:
                        try:
                            cut_img.save(f"{basic_file}/{eposide_title}/{la}/{n}.jpg")
                        except:
                            print(f'didnt save {basic_file}/{eposide_title}/{la}/{n}.jpg')
                    cut_img_y = j
                    num = 0
                    n += 1
            la += 1
            shutil.rmtree(basic_file + flod_path, ignore_errors=True)

def reply(final_arr):
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    for j in range(int(len(final_arr) / 4)):
        p1.append(j)
    for k in range(int(len(final_arr) / 4)):
        p2.append(k + p1[int(len(final_arr) / 4) - 1] + 1)
    for l in range(int(len(final_arr) / 4)):
        p3.append(l + p2[int(len(final_arr) / 4) - 1] + 1)
    for z in range(len(final_arr) - (len(p3) * 3)):
        p4.append(z + p3[int(len(final_arr) / 4) - 1] + 1)

    return p1, p2, p3, p4

if __name__ == '__main__':
    url = 'https://comic.naver.com/webtoon/weekday'

    html = urllib.request.urlopen(url)
    Soup = BeautifulSoup(html.read(), "html.parser")
    html.close()

    get_main_url = Soup.select('a')
    main_page_url = []
    for get_main_url in get_main_url:

        i = get_main_url['href']

        if 'titleId' in i:
            if 'weekday' in i:
                main_page_url.append('https://comic.naver.com' + str(i))

    url_arr = main_page_url

    brr = [reply(url_arr)]
    pool = multiprocessing.Pool(processes=4)
    for i in range(3):
        pool.map(downloader, brr[i])
        pool.close()
        pool.join()
    print('done work')
