# News Aggregator & Summarizer API

A FastAPI-based news aggregation service that scrapes, categorizes, and summarizes news articles.

## Features
- News scraping from multiple sources
- Article categorization using OpenAI
- Article summarization
- Search functionality
- Category-based filtering
- Sorting by date, title, and source

## Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key
   NEWS_API_KEY=your_news_api_key
   ```
5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints
- `GET /`: Welcome message
- `GET /news`: Get news articles with optional parameters:
  - `summarize`: Boolean to include article summaries
  - `query`: Search term
  - `categories`: Filter by categories
  - `sort_by`: Sort by date, title, or source
  - `order`: Sort order (asc/desc)

## License
MIT 