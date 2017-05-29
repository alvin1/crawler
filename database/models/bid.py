#
# 表名：bid
# 说明：标的表，用来存储中标结果列表
#

from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BID(Base):
    __tablename__ = 'bid'

    id = Sequence()