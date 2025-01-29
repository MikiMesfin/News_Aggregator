from openai import AsyncOpenAI, OpenAIError
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class ArticleSummarizer:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def summarize(self, text: str, max_length: int = 150) -> str:
        try:
            if not text:
                return "No content to summarize"
                
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes news articles concisely."},
                    {"role": "user", "content": f"Summarize this news article in about {max_length} words: {text}"}
                ],
                max_tokens=200,
                temperature=0.5
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return f"Error generating summary: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error during summarization: {str(e)}")
            return "An unexpected error occurred during summarization"