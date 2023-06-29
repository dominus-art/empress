from sqlalchemy import Column, Integer, String

from database import Base


class Truth(Base):
    __tablename__ = "truth_questions"
    id = Column(Integer, nullable=False, index=True, primary_key=True)
    rating = Column(Integer, nullable=False, index=True)
    question = Column(String)


class Dare(Base):
    __tablename__ = "dares"
    id = Column(Integer, nullable=False, index=True, primary_key=True)
    rating = Column(Integer, nullable=False, index=True)
    dare = Column(String)
