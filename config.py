import os

DB_URI = 'mysql://root:QingTing0108@localhost:3306/m?charset=utf8mb4'
REDIS_DB = 0
REDIS_HOST = 'localhost'
REDIS_PORT = 6379


PROXIES = []
HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DB = os.path.join(HERE, 'data/fake_useragent.json')



DISCOVER_URL = 'http://music.163.com/discover/artist/cat?id={}&initial={}'
ARTIST_URL = 'http://music.163.com/artist?id={}'  #歌手
SONG_URL = 'http://music.163.com/song?id={}'  #歌曲详情页面
COMMENTS_URL = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}'  # noqa
