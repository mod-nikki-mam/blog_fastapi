from sqlalchemy import Column, Any, ForeignKey, Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database_handling import Base


class Entry(Base):
    __tablename__ = "entry"
    id = Column(Integer, primary_key=True, index=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"))
    link = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=True)
    title = Column(String, index=True, nullable=True)
    summary = Column(Text, nullable=True)
    published = Column(DateTime, nullable=True)
    feed = relationship("Feeds", back_populates="entries")


class Feeds(Base):
    __tablename__ = "feeds"
    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, nullable=False)
    success = Column(Boolean, default=False, nullable=False, index=True)
    title = Column(String, nullable=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    entries = relationship("Entry", back_populates="feed")
    error = Column(String, nullable=True)
