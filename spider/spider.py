import time
import imp

from ext import session
from models.models import User, Art, Song, Comment
from config import DISCOVER_URL, ARTIST_URL, SONG_URL, COMMENTS_URL
from .utils import get_tree, post

import encodings


def parser_artist_list(cat_id, initial_id):
    tree = get_tree(DISCOVER_URL.format(cat_id, initial_id))
    artist_items = tree.xpath('//a[contains(@class, "nm-icn")]/@href')

    return [item.split('=')[1] for item in artist_items]


def parser_artist(artist_id):
    tree = get_tree(ARTIST_URL.format(artist_id))
    art = session.query(Art).filter_by(id=artist_id).all()
    print(art)
    if not art:
        art_name = str(tree.xpath('//h2[@id="artist-name"]/text()')[0])
        picture = str(tree.xpath(
            '//div[contains(@class, "n-artist")]//img/@src')[0])
        art = Art(
            id = artist_id,
            name= art_name,
            picture= picture
        )
        session.add(art)
        session.commit()
    else:
        art = art[0]
    song_items = tree.xpath('//div[@id="artist-top50"]//ul/li/a/@href')
    for item in song_items:
        song_id = item.split('=')[1]
        song = session.query(Song).filter_by(id=song_id).all()
        if not song:
            song = parser_song(song_id, art)
            session.add(song)
            session.commit()
        else:
            time.sleep(1)



def parser_song(song_id, art):
    tree = get_tree(SONG_URL.format(song_id))
    song = session.query(Song).filter_by(id=song_id).all()
    r = post(COMMENTS_URL.format(song_id))
    if r.status_code != 200:
        print('API error: Song: {}'.format(song_id))
        return
    data = r.json()
    if not song:
        for404 = tree.xpath('//div[@class="n-for404"]')
        if for404:
            return
        try:
            song_name = tree.xpath('//em[@class="f-ff2"]/text()')[0].strip()
        except IndexError:
            try:
                song_name = tree.xpath(
                    '//meta[@name="keywords"]/@content')[0].strip()
            except IndexError:
                print('Fetch limit!')
                time.sleep(10)
                return parser_song(song_id, art)
        song = Song(
            id = song_id,
            name=str(song_name),
            art_id=art.id,
            comment_count=int(data['total'])
        )
        session.add(song)
        session.commit()
    else:
        song = song[0]
    for comment_ in data['hotComments']:
        comment_id = comment_['commentId']
        content = comment_['content']
        like_count = comment_['likedCount']
        user_ = comment_['user']
        if not user_:
            continue
        user = session.query(User).filter_by(id=user_['userId']).all()
        if not user:
            user = User(
                id = user_['userId'],
                name=user_['nickname'],
                picture=user_['avatarUrl']
            )
            try:
                session.add(user)
                session.commit()
            except Exception as e:
                continue
        else:
            user = user[0]
        comment = session.query(Comment).filter_by(id=comment_id).all()
        if not comment:
            comment = Comment(
                id=comment_id,
                use_id=user.id,
                song_id=song.id,
                content=content,
                like_count=like_count
            )
            session.add(comment)
            session.commit()
    return song