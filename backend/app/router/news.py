from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from newsapi import NewsApiClient
from app import models, schemas, database, config
from enum import Enum
from app import utils, oauth2
from app.ml_model import get_recommendations
import random
from collections import defaultdict

router = APIRouter(
    tags=["news"],
    prefix= "/news"
)

newsapi = NewsApiClient(api_key=f'{config.settings.news_api_key}')

class Category(str, Enum):
    general = 'general'
    business = 'business'
    entertainment = 'entertainment'
    science = 'science'
    sports = 'sports'
    technology = 'technology'
    health = 'health'
    
    

                                                                        
@router.get("/", response_model= list[schemas.NewsArticleFromDB])
async def get_news_articles(db: Session = Depends(database.get_db)  ,current_user: int = Depends(oauth2.get_current_user)):
    
    existing_titles = set(
        article.title for article in db.query(models.NewsArticle.title).all()
    )

    new_articles = []
    for category in Category:
        articles = utils.get_articles_by_category(category, limit=5)
        for article in articles:
            if article.title not in existing_titles:
                new_articles.append(models.NewsArticle(**article.dict()))
                existing_titles.add(article.title)  # Add to set to avoid re-checking

    # Bulk insert new articles
    if new_articles:
        db.bulk_save_objects(new_articles)
        db.commit()

    return db.query(models.NewsArticle).all()

    # for category in Category:
    #     articles = utils.get_articles_by_category(category, limit= 2)
    #     for article in articles:
    #         existing_article = db.query(models.NewsArticle).filter(models.NewsArticle.title == article.title).first()
    #         if not existing_article:
    #             db.add(models.NewsArticle(**article.dict()))
    
    # db.commit()
    # return db.query(models.NewsArticle).all()

  
  
@router.post("/activity")
async def record_activity(activity: schemas.UserActivity,db: Session = Depends(database.get_db) , current_user: int = Depends(oauth2.get_current_user)):
    if not db.query(models.NewsArticle).filter(models.NewsArticle.id == activity.article_id).first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Article not found")
    #check if for the current user id there is view and read both
    existing_activities = db.query(models.UserActivity).filter(
        models.UserActivity.article_id == activity.article_id,
        models.UserActivity.user_id == current_user.id
    ).all()
    existing_activity_types = {activ.action for activ in existing_activities}
    if activity.action in existing_activity_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="like or read activities already exist for this article and user.")
    
    new_activity = models.UserActivity(user_id = current_user.id ,**activity.dict())
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity
    
    
      

@router.get("/recommended")
async def get_recommended_news_articles( current_user: int = Depends(oauth2.get_current_user),db: Session = Depends(database.get_db) ):
    # we need to check from user_activity table that what kind of article does this user like and read, basically categories of those articles
    user_liked_catgories_table = db.query(models.UserActivity, models.NewsArticle.category).join(
                                          models.NewsArticle, models.UserActivity.article_id == models.NewsArticle.id, isouter= True).filter(
                                          models.UserActivity.user_id == current_user.id).all()
    liked_categories = defaultdict(int)
    likings_with_count  = [] 
    for row in user_liked_catgories_table:
        liked_categories[row.category] += 1    
    for category, count in liked_categories.items():
        likings_with_count.append((category, count))           
                  
    # #find top 2 categories
    # print(likings_with_count)
    # top_2_categories = sorted(liked_categories.items(), key=lambda x: x[1], reverse=True)[:2]
    # top_2_category_names = [category for category, _ in top_2_categories]
    # print(top_2_category_names)
    
    articles = [ schemas.NewsArticleForRecommendations(title= row.title, category= row.category, id= row.id) for row in db.query(models.NewsArticle).all()]
    random_articles = random.sample(articles, 15)
    
    recommended_articles = await get_recommendations(articles= random_articles, user_likings= likings_with_count)
    return recommended_articles
    


          
@router.get("/{category}", response_model= list[schemas.NewsArticleResponse])
async def get_news_articles_by_category(category: Category, current_user: int = Depends(oauth2.get_current_user)):
    return utils.get_articles_by_category(category= category.value, limit= 20)
       


