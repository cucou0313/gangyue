from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('mysql+pymysql://root:0313@localhost/gangyue')
# pythonanywhere
# engine = create_engine(
#     'mysql+pymysql://cucou0313:gangyue6@cucou0313.mysql.pythonanywhere-services.com/cucou0313$gangyue'
# )
DBsession = sessionmaker(bind=engine)
session = DBsession()

Base = declarative_base()


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(Text, nullable=False)
    category = Column(String(20), nullable=False)
    added_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    is_active = Column(Integer, nullable=False, default=1)
    is_knot = Column(Integer, nullable=False, default=0)


category = ['觅食', '运动', '学习', '娱乐']
for i in range(1, 100):
    post = Post(title='test%s' % i,
                category=category[i % 4],
                added_time=datetime.datetime.now(),
                user_id=i % 3 + 1)
    # print(post.title, post.category, post.added_time, post.user_id)
    session.add(post)
session.commit()
session.close()

# session.add_all([student1, student2, student3])
# session.commit()
# session.close()
