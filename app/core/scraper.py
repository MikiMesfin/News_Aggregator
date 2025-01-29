from bs4 import BeautifulSoup
import requests
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        self.sources = {
            'bbc': 'https://www.bbc.com/news',
            'cnn': 'https://www.cnn.com',
        }
        
    def scrape_article(self, url: str) -> Dict:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Basic extraction - you'll need to customize based on each site's structure
            title = soup.find('h1').text.strip() if soup.find('h1') else ''
            content = ' '.join([p.text for p in soup.find_all('p')])
            
            return {
                'title': title,
                'content': content,
                'url': url
            }
        except Exception as e:
            logger.error(f"Error scraping article {url}: {str(e)}")
            return {}

    def get_latest_news(self) -> List[Dict]:
        articles = []
        for source, url in self.sources.items():
            try:
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Example for BBC - you'll need to customize for each source
                if source == 'bbc':
                    links = soup.find_all('a', class_='gs-c-promo-heading')
                    for link in links[:5]:  # Get first 5 articles
                        article_url = f"https://www.bbc.com{link['href']}"
                        article = self.scrape_article(article_url)
                        if article:
                            article['source'] = source
                            articles.append(article)
                            
            except Exception as e:
                logger.error(f"Error scraping {source}: {str(e)}")
                
        return articles