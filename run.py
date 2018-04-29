import itertools
from spider.spider import parser_artist_list, parser_artist
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

CAT_IDS = [1001,]# 1002, 1003, 2001, 2002, 2003, 4001, 4002, 4003,
           #6001, 6002, 6003, 7001, 7002, 7003]
INITIAL_IDS = [0, -1] + list(range(65, 91))


with ProcessPoolExecutor() as excutor:
    for product in itertools.product(CAT_IDS, INITIAL_IDS):
        for artist_id in parser_artist_list(*product):
            excutor.map(parser_artist, [artist_id, ])




