from datetime import datetime

from sqlalchemy import Table, Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr, AbstractConcreteBase



from ext import Base, eng


class BaseModel(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime)


class User(BaseModel):
    __tablename__ = 'user'
    name = Column(String(128))
    picture = Column(String(1024))



class Art(BaseModel):
    __tablename__ = 'art'
    name = Column(String(256))
    picture = Column(Text)


class Song(BaseModel):
    __tablename__ = 'song'
    name = Column(String(256))
    comment_count = Column(Integer)
    art_id = Column(Integer, ForeignKey('art.id'))
    art = relationship('Art', back_populates='songs')

Art.songs = relationship('Song', order_by=Song.id, back_populates='art')

class Comment(BaseModel):
    __tablename__ = 'comment'
    content = Column(Text)
    like_count = Column(Integer)
    use_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')
    song_id = Column(Integer, ForeignKey('song.id'))
    song = relationship('Song', back_populates='comments')

Song.comments = relationship('Comment', order_by=Comment.id, back_populates='song')


def init_db():
    Base.metadata.create_all(bind=eng)






def drop_db():
    Base.metadata.drop_all(bind=eng)


if __name__ == '__main__':
    drop_db()
    init_db()





