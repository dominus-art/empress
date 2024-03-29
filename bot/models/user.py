from sqlalchemy import Column, Integer, String, BigInteger, Boolean
import json

from database import Base


class User(Base):
    __tablename__ = "users"
    discord_id = Column(BigInteger, nullable=False, index=True, primary_key=True)
    bad_words = Column(String, default=json.dumps([]))
    lives = Column(Integer, default=-1)
    role_lock = Column(Boolean, default=False)
