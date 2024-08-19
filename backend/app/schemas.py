from pydantic import BaseModel, EmailStr
from app import models
from datetime import datetime
from typing import Union

class NewsArticleResponse(BaseModel):
    title: str
    url: str
    author: str
    category: str
    publishedAt: datetime
    
class NewsArticleFromDB(NewsArticleResponse):    
    id:int
    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str    
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str    
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime   

class Token(BaseModel):
    access_token: str
    token_type: str    

class TokenData(BaseModel):
    id: str | None = None    
            
class UserActivity(BaseModel):
    action: str 
    article_id: int       
    
class NewsArticleForRecommendations(BaseModel):  
    id: int
    title: str
    category: str  