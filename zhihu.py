import os
import requests
from pyquery import PyQuery as pq

from utils import log

from config import cookie
from config import authorization


class Model():
    """
    基类, 用来显示类的信息
    """

    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):
    """
    存储电影信息
    """

    def __init__(self):
        self.name = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0


def cached_url(url):
    """
    缓存, 避免重复下载网页浪费时间
    """
    folder = 'cached'
    filename = '{}.html'.format(url.split('=', 1)[-1])
    # /
    # \
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
        return s
    else:
        # 建立 cached 文件夹
        if not os.path.exists(folder):
            os.makedirs(folder)
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/59.0.3071.115 Safari/537.36',
        'authorization': authorization,
        'Cookie': cookie
    }

    r = requests.get(url, headers=headers)
    page = r.json()
    return page


def download_image(url, filename):
    # 通过 url 获取到该图片的数据并写入文件
    r = requests.get(url)

    folder = 'image'
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, filename)

    with open(path, 'wb') as f:
        f.write(r.content)


def save_cover(movies):
    for m in movies:
        filename = '{}.jpg'.format(m.ranking)
        download_image(m.cover_url, filename)


def timeline_from_url(url):
    page = get(url)
    log(page)


def main():
    url = 'your url'
    timeline_from_url(url)


if __name__ == '__main__':
    main()
