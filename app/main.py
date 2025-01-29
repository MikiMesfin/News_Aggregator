from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.core.scraper import NewsScraper
from app.core.summarizer import ArticleSummarizer
from app.core.categorizer import ArticleCategorizer
from typing import Optional, List

app = FastAPI(title="News Aggregator & Summarizer")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scraper = NewsScraper()
summarizer = ArticleSummarizer()
categorizer = ArticleCategorizer()

@app.get("/")
async def root():
    return {"message": "Welcome to News Aggregator API"}

@app.get("/news")
async def get_news(
    summarize: bool = False,
    query: Optional[str] = Query(None, description="Search query for filtering articles"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories"),
    sort_by: Optional[str] = Query(None, description="Sort by: date, title, source"),
    order: Optional[str] = Query("desc", description="Sort order: asc or desc")
):
    try:
        articles = scraper.get_latest_news()
        
        # Categorize articles
        for article in articles:
            if article.get('title') and article.get('content'):
                article['categories'] = await categorizer.categorize(
                    article['title'], 
                    article['content']
                )
        
        # Filter by categories if specified
        if categories:
            articles = [
                article for article in articles
                if any(cat in article.get('categories', []) for cat in categories)
            ]
        
        # Filter by search query if specified
        if query:
            articles = [
                article for article in articles
                if query.lower() in article.get('title', '').lower() 
                or query.lower() in article.get('content', '').lower()
            ]
        
        # Summarize if requested
        if summarize:
            for article in articles:
                if article.get('content'):
                    article['summary'] = await summarizer.summarize(article['content'])
        
        # Sort articles
        if sort_by:
            reverse = order.lower() == "desc"
            if sort_by == "date":
                articles.sort(key=lambda x: x.get('published_at', ''), reverse=reverse)
            elif sort_by == "title":
                articles.sort(key=lambda x: x.get('title', ''), reverse=reverse)
            elif sort_by == "source":
                articles.sort(key=lambda x: x.get('source', ''), reverse=reverse)
        
        return {"articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categories")
async def get_categories():
    """Get list of available categories"""
    return {"categories": categorizer.categories}
