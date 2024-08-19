from newsapi import NewsApiClient
from app import models, schemas
from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



newsapi = NewsApiClient(api_key='ba4e3f267d624b4ba13d6856f80a91eb')


def get_articles_by_category(category: str,limit: int):   
    top_headlines = newsapi.get_top_headlines( category= category,  language='en',  country='us', page_size= limit)
    articles = top_headlines.get('articles')
    if not articles:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "article not found")
    transformed_articles = [
        schemas.NewsArticleResponse(
            title=article.get('title', ''),
            url=article.get('url', ''),
            author=article.get('author', ''),
            category=category, 
            publishedAt= article.get('publishedAt', ''),
        )
        for article in articles
    ]
    return transformed_articles


def hashPassword(password: str):
    return pwd_context.hash(password)

def verifyPassword(hashed_password: str, plain_password: str):
    return pwd_context.verify(plain_password, hashed_password)