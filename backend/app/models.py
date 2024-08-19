from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text, TIMESTAMP
from app.database import Base


class UserActivity(Base):
    __tablename__ = "user_activity"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete= "CASCADE"), nullable=False)
    action = Column(String, nullable= False)
    article_id = Column(Integer, ForeignKey('news_articles.id', ondelete= "CASCADE"), nullable=False)
   
    

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))



class NewsArticle(Base):
    __tablename__ = 'news_articles'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    url = Column(String, nullable=False)
    category = Column(String, nullable=False)
    publishedAt = Column(TIMESTAMP(timezone=True), nullable=False)
    