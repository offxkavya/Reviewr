from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
import datetime
from app.db.session import Base

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    github_pr_id = Column(String(100), index=True)
    title = Column(Text)
    repository = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    pr_id = Column(Integer, ForeignKey("pull_requests.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    review_type = Column(String(50))
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    line_number = Column(Integer, nullable=True)
    severity = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
