from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import multiprocessing
import shutil
import numpy as np
import os


def downloader(ls):
    for lang in ls:
        print(lang)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        number = 1
        arr = []
        inputer = lang
        if 'no' in inputer:
            url = inputer
            ider = url[47:53]
            weekday = url[68:]
            adap = "https://comic.naver.com/webtoon/list?titleId=" + str(ider) + "&weekday=" + str(weekday)
        else:
            url = inputer
            ider = url[45:51]
            weekday = url[60:]
            adap = url
        html1 = urllib.request.urlopen(adap)
        Soup1 = BeautifulSoup(html1.read(), "html.parser")
        html1.close()
        get__url = Soup1.select('a')
        get_title = Soup1.select('.title')
        eposide_title = str(get_title[0]).lstrip('<span class="title">').rstrip('</span>')
        k = 0
        for get__url in get__url:
            k += 1
            url_i = get__url['href']
            if k % 2 == 0:
                if 'weekday' in url_i:
                    if 'no' in url_i:
                        nu = (url_i.lstrip(f'/webtoon/detail?titleId={ider}').lstrip(r'&no=').rstrip(weekday).rstrip(
                            r'&weekday='))
                        arr.append(int(nu))
        maxValue = np.max(arr)
        brr1 = []
        for no in range(int(maxValue)):
            edit = "https://comic.naver.com/webtoon/detail?titleId=" + ider + "&no=" + str(no+1) + "&weekday=" + weekday
            brr1.append(edit)
        la = 1
        basic_file = os.getcwd().replace("\\", "/")
        new_img = None
        flod_path = str(ider)
        for epsoide in brr1:
            if la == maxValue+1:
                print(f'{eposide_title} is overflow')
            print(f"{eposide_title} {la}/{maxValue}화 작업중")
            try:
                os.makedirs(f"{basic_file}/webtoon/{eposide_title}/{la}")
            except (Exception,):
                print(f'didnt make {basic_file}/webtoon/{eposide_title}/{la}')
            try:
                os.mkdir("webtoon/"+flod_path)
            except (Exception,):
                pass
            custom_img = []
            html2 = urllib.request.urlopen(epsoide)
            Soup2 = BeautifulSoup(html2.read(), "html.parser")
            html2.close()
            img_url = Soup2.select('img')
            for img_url in img_url:
                get_j = img_url.get('src')
                if get_j is None:
                    pass
                elif 'IMAG01' in get_j:
                    custom_img.append(get_j)
            down_num = 0
            img_arr = []
            for image_url in custom_img:
                down_num += 1
                img_path = basic_file + "/webtoon" + f"/{flod_path}/" + str(down_num) + '.jpg'
                urllib.request.urlretrieve(image_url, img_path)
                img_arr.append(img_path)
            number += 1
            for re in range(len(img_arr) - 1):
                if re == 0:
                    first_img = Image.open(img_arr[re])
                else:
                    first_img = new_img
                second_img = Image.open(img_arr[re + 1])
                first_img_size = first_img.size
                second_img_size = second_img.size
                new_img = Image.new('RGB', (first_img_size[0], first_img_size[1] + (second_img_size[1])),
                                    (255, 255, 255))
                new_img.paste(first_img, (0, 0))
                new_img.paste(second_img, (0, first_img_size[1]))
            n = 1
            cut_img_y = 0
            img = new_img
            pix = np.array(img)
            counter = 0
            for pixel_y in range(img.size[1]):
                judge = pix[pixel_y][np.arange(0, img.size[0])]
                if np.max(judge) == np.min(judge) == 255 or \
                        np.max(judge) == np.min(judge) == 0:
                    counter += 1
                if counter == 300:
                    cut_img = img.crop((0, cut_img_y, img.size[0], pixel_y))
                    if int(cut_img.size[1]) <= 300:
                        n = n - 1
                    else:
                        if cut_img.size[1] >= 50000:
                            print('image overflow')
                            n += 1
                            back_img = Image.new('RGB', (0, int(cut_img.size[1]) / 2), (255, 255, 255))
                            back_second_img = Image.new('RGB', (0, int(cut_img.size[1]) / 2), (255, 255, 255))
                            back_img.paste(cut_img, 0, cut_img.size[1] / 2)
                            back_second_img.paste(cut_img, 0, cut_img.size[1])
                            back_img.save(f"{basic_file}/webtoon/{eposide_title}/{la}/{n - 1}.jpg")
                            back_second_img.save(f"{basic_file}/{eposide_title}/{la}/{n}.jpg")
                        else:
                            cut_img.save(f"{basic_file}/webtoon/{eposide_title}/{la}/{n}.jpg")
                    cut_img_y = pixel_y
                    counter = 0
                    n += 1
            la += 1
            shutil.rmtree(basic_file + flod_path, ignore_errors=True)


def reply(arag, numer):
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


if __name__ == '__main__':
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
    num = multiprocessing.cpu_count()
    brr = [reply(url_arr, num)]
    pool = multiprocessing.Pool(processes=num)
    for i in range(int(num)):
        pool.map(downloader, brr[i])
        pool.close()
        pool.join()
    print('done work')
