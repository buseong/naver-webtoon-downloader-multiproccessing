import argparse
import multiprocessing
from module import get_url, etc
import os
import shutil
import urllib.request
import numpy as np
from module.etc import get_soup, get_id_wk
from module.image_edit import img_add, overpx_edit


def downloader(ls):
    for lang in ls:
        print(lang)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        number = 1
        la = 1
        k = 0
        arr = []
        brr1 = []
        basic_path = os.getcwd().replace("\\", "/")
        adap, ider, weekday = get_id_wk(lang)
        Soup1 = get_soup(adap)
        get__url = Soup1.select('a')
        get_title = Soup1.select('.title')
        eposide_title = str(get_title[0]).lstrip('<span class="title">').rstrip('</span>')
        for get__url in get__url:
            k += 1
            url_i = get__url['href']
            if k % 2 == 0:
                if 'weekday' in url_i:
                    if 'no' in url_i:
                        nu = (url_i.lstrip(f'/{base_folder}/detail?titleId={ider}').lstrip(r'&no=').rstrip(weekday).
                              rstrip(r'&weekday='))
                        arr.append(int(nu))
        maxValue = np.max(arr)
        for no in range(int(maxValue)):
            edit = "https://comic.naver.com/webtoon/detail?titleId=" + ider + "&no=" + str(no+1) + "&weekday=" + weekday
            brr1.append(edit)
        folder_path = str(ider)
        for epsoide in brr1:
            print(f"{eposide_title} {la}/{maxValue}화 작업중")
            try:
                os.makedirs(f"{basic_path}/{base_folder}/{eposide_title}/{la}")
            except (Exception,):
                print(f'didnt make {basic_path}/{base_folder}/{eposide_title}/{la}')
            try:
                os.mkdir(f"{basic_path}/{base_folder}/" + folder_path)
            except (Exception,):
                pass
            custom_img = []
            Soup2 = get_soup(epsoide)
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
                img_path = basic_path + f"/{base_folder}" + f"/{folder_path}/" + str(down_num) + '.jpg'
                urllib.request.urlretrieve(image_url, img_path)
                img_arr.append(img_path)
            number += 1
            img = img_add(img_arr)
            n = 1
            cut_img_y = 0
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
                            overpx_edit(cut_img, basic_path, base_folder, eposide_title, la, n)
                        else:
                            cut_img.save(f"{basic_path}/{base_folder}/{eposide_title}/{la}/{n}.jpg")
                    cut_img_y = pixel_y
                    counter = 0
                    n += 1
            la += 1
            shutil.rmtree(basic_path + folder_path, ignore_errors=True)
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='naver-webtoon-downloader',
                                     epilog='naver webtoon downloader multiprocessing')
    parser.add_argument('-f', '--folder', required=False, help='image download folder', default='webtoon')
    args = parser.parse_args()
    global base_folder
    base_folder = args.folder
    print(base_folder)
    url_arr = get_url.get_all_wt()
    num = multiprocessing.cpu_count()
    brr = [etc.sort_num(url_arr, num)]
    pool = multiprocessing.Pool(processes=num)
    # for i in range(int(num)):
    #     pool.map(downloader, brr[i])
    #     pool.close()
    #     pool.join()
    # print('done work')
