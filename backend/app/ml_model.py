from app import schemas, models
import google.generativeai as genai
import json
from app.config import settings



genai.configure(api_key=f"{settings.gemini_api_key}")

  
async def get_recommendations(articles: list[schemas.NewsArticleForRecommendations], user_likings: list[tuple]):
 
    model = genai.GenerativeModel(
                                    'gemini-1.5-pro',
                                    generation_config= {
                                        "response_mime_type": "application/json",
                                         "response_schema": list[schemas.NewsArticleForRecommendations]
                                    }
                                 )
   
    likings_str = ', '.join([f"Category: {liking[0]}, liking: {liking[1]}" for liking in user_likings])
    articles_str = '\n'.join([f"Id: {article.id} , Title: {article.title}, Category: {article.category}" for article in articles])
   
   
    prompt = f"""
    You are an AI model trained to recommend articles. Below is a list of articles, each with a title, category. Also provided is a list of user likings, which indicates the categories and liking of the user.

    Based on this information, recommend a list of articles that align with the user's preferences. The recommendations should prioritize articles that match the user's favorite categories or topics. If multiple articles fit, recommend the ones with the highest relevance.

    User Likings:
    {likings_str}

    Articles List:
    {articles_str}

    Recommend articles for this user:
    """
    response = model.generate_content(prompt)
    return json.loads(response.text)