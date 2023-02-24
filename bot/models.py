from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY

from db import Base


class User(Base):
    __tablename__ = "users"

    discord_id = Column(Integer, primary_key=True, nullable=False, index=True)
    owned_by = Column(Integer, index=True, default=0)
    properties = Column(ARRAY(Integer), default=[])
    bad_words = Column(ARRAY(String), default=[])
    claimed_by = Column(Integer, index=True, default=0)
    lives = Column(Integer, default=-1)
