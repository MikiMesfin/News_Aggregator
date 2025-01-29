from openai import AsyncOpenAI, OpenAIError
from app.config import settings
import logging
from typing import List

logger = logging.getLogger(__name__)

class ArticleCategorizer:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.categories = [
            "Technology", "Politics", "Business", "Science",
            "Health", "Sports", "Entertainment", "World News"
        ]

    async def categorize(self, title: str, content: str) -> List[str]:
        try:
            prompt = f"Categorize this article into one or more of these categories: {', '.join(self.categories)}.\n\nTitle: {title}\nContent: {content}"
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that categorizes news articles. Respond only with comma-separated categories."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.3
            )
            
            categories = [cat.strip() for cat in response.choices[0].message.content.split(',')]
            return [cat for cat in categories if cat in self.categories]
            
        except OpenAIError as e:
            logger.error(f"OpenAI API error during categorization: {str(e)}")
            return ["Uncategorized"]
        except Exception as e:
            logger.error(f"Unexpected error during categorization: {str(e)}")
            return ["Uncategorized"] 