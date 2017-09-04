import os
import requests
from pyquery import PyQuery as pq


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
        self.point = 0
        self.cover_url = ''
        self.ranking = 0


def cached_url(url):
    """
    缓存, 避免重复下载网页浪费时间
    """
    folder = 'cached'
    if '-' in url:
        filename = '{}'.format(url.split('-', 1)[-1])
    else:
        filename = '1.html'
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
    return cached_url(url)


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


def movie_from_div(div):
    """
    从一个 div 里面获取到一个电影信息
    """
    e = pq(div)

    m = Movie()
    m.name = e('h2 a').text()
    m.point = e('.total').text().strip() + e('.total2').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.number em').text()
    return m


def movies_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    page = get(url)
    e = pq(page)
    items = e('#asyncRatingRegion li')
    # 调用 movie_from_div
    movies = [movie_from_div(i) for i in items]
    return movies


def main():
    for i in range(1, 11):
        if i == 1:
            url = 'http://www.mtime.com/top/movie/top100/'
        else:
            url = 'http://www.mtime.com/top/movie/top100/index-{}.html'.format(i)
        movies = movies_from_url(url)
        print('top100 movies', movies)
        save_cover(movies)


def test():
    m = Movie()
    m.name = '100'
    m.cover_url = 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p984732992.jpg'
    save_cover([m])


if __name__ == '__main__':
    # test()
    main()
