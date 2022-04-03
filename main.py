import argparse
import multiprocessing
from module import naver_wt_downloader, get_url, etc

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='naver-webtoon-downloader')
    parser.add_argument('--folder', required=False, help='image downloader folder', default='webtoon')
    args = parser.parse_args()
    url_arr = get_url.get_all_wt()
    num = multiprocessing.cpu_count()
    brr = [etc.sort_num(url_arr, num)]
    pool = multiprocessing.Pool(processes=num)
    for i in range(int(num)):
        pool.map(naver_wt_downloader.downloader, brr[i])
        pool.close()
        pool.join()
    print('done work')
