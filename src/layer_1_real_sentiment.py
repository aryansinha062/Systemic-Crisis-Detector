"""
Layer 1: Real News Sentiment Integration
Fetches live headlines from NewsAPI and analyzes sentiment
"""

import requests
from datetime import datetime, timedelta
from textblob import TextBlob
import os

class RealNewssentimentDetector:
    
    def __init__(self):
        self.timestamp = datetime.now()
        # For free tier, we'll use mock but structure for real API
        self.use_real_api = False  # Set to True when you add NewsAPI key
        self.newsapi_key = os.getenv('NEWSAPI_KEY', '')
        self.newsapi_url = 'https://newsapi.org/v2/everything'
    
    def fetch_real_headlines(self, ticker, days=7):
        """
        Fetch real headlines from NewsAPI
        Free tier: 100 requests/day, 1 month history
        """
        if not self.use_real_api or not self.newsapi_key:
            return self.get_mock_headlines(ticker)
        
        try:
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            params = {
                'q': ticker,
                'from': from_date,
                'sortBy': 'publishedAt',
                'apiKey': self.newsapi_key,
                'language': 'en'
            }
            
            response = requests.get(self.newsapi_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            return {
                'ticker': ticker,
                'articles_count': len(articles),
                'articles': [{'title': a['title'], 'source': a['source']['name']} for a in articles[:10]],
                'source': 'NewsAPI (REAL)'
            }
        except Exception as e:
            print(f"API Error: {e}. Falling back to mock data.")
            return self.get_mock_headlines(ticker)
    
    def get_mock_headlines(self, ticker):
        """Mock headlines for demonstration"""
        mock_data = {
            'TSLA': {
                'articles': [
                    {'title': 'Tesla Q2 deliveries miss expectations', 'source': 'Reuters'},
                    {'title': 'Elon Musk sells $4B worth of Tesla stock', 'source': 'Bloomberg'},
                    {'title': 'Tesla faces supply chain disruptions', 'source': 'CNBC'},
                    {'title': 'Tesla stock falls on profit warning', 'source': 'MarketWatch'},
                    {'title': 'Competitor BYD overtakes Tesla in EV sales', 'source': 'WSJ'}
                ],
                'trend': 'NEGATIVE'
            },
            'AAPL': {
                'articles': [
                    {'title': 'Apple beats revenue expectations in Q2', 'source': 'Reuters'},
                    {'title': 'iPhone 16 launch anticipation builds', 'source': 'Bloomberg'},
                    {'title': 'Apple services segment reaches all-time high', 'source': 'CNBC'},
                    {'title': 'Warren Buffett increases Apple stake', 'source': 'MarketWatch'},
                    {'title': 'Apple announces $110B buyback program', 'source': 'WSJ'}
                ],
                'trend': 'POSITIVE'
            },
            'META': {
                'articles': [
                    {'title': 'Meta lays off 10,000 more employees', 'source': 'Reuters'},
                    {'title': 'Meta stock drops on AI investment concerns', 'source': 'Bloomberg'},
                    {'title': 'Reality Labs division loses $13.7B in 2024', 'source': 'CNBC'},
                    {'title': 'Meta faces regulatory scrutiny in EU', 'source': 'MarketWatch'},
                    {'title': 'TikTok competition pressures Meta growth', 'source': 'WSJ'}
                ],
                'trend': 'NEGATIVE'
            }
        }
        
        data = mock_data.get(ticker, {'articles': [], 'trend': 'NEUTRAL'})
        
        return {
            'ticker': ticker,
            'articles_count': len(data['articles']),
            'articles': data['articles'],
            'source': 'Mock Headlines (demonstration)'
        }
    
    def analyze_sentiment(self, headlines):
        """
        Analyze sentiment of headlines using TextBlob
        Returns score from -1.0 (very negative) to +1.0 (very positive)
        """
        if not headlines:
            return 0.0
        
        sentiments = []
        for article in headlines:
            title = article.get('title', '')
            if title:
                try:
                    blob = TextBlob(title)
                    sentiments.append(blob.sentiment.polarity)
                except:
                    pass
        
        if sentiments:
            return sum(sentiments) / len(sentiments)
        return 0.0
    
    def get_sentiment_alert(self, score):
        """Convert sentiment score to alert level"""
        if score < -0.3:
            return 'CRITICAL'
        elif score < 0.0:
            return 'WARNING'
        elif score < 0.3:
            return 'NORMAL'
        else:
            return 'HEALTHY'
    
    def analyze_ticker(self, ticker, days=7):
        """Full sentiment analysis for a ticker"""
        headlines_data = self.fetch_real_headlines(ticker, days)
        headlines = headlines_data['articles']
        
        sentiment_score = self.analyze_sentiment(headlines)
        alert = self.get_sentiment_alert(sentiment_score)
        
        return {
            'ticker': ticker,
            'sentiment_score': round(sentiment_score, 3),
            'alert': alert,
            'articles_analyzed': headlines_data['articles_count'],
            'top_headlines': headlines[:3],
            'data_source': headlines_data['source'],
            'timestamp': self.timestamp
        }


if __name__ == '__main__':
    detector = RealNewssentimentDetector()
    
    print("\n=== LAYER 1: REAL NEWS SENTIMENT ANALYSIS ===\n")
    
    for ticker in ['TSLA', 'AAPL', 'META']:
        result = detector.analyze_ticker(ticker, days=7)
        print(f"\n--- {ticker} ---")
        print(f"Sentiment Score: {result['sentiment_score']}")
        print(f"Alert Level: {result['alert']}")
        print(f"Articles Analyzed: {result['articles_analyzed']}")
        print(f"Data Source: {result['data_source']}")
        print(f"Top Headlines:")
        for i, article in enumerate(result['top_headlines'][:2], 1):
            print(f"  {i}. {article['title']} ({article['source']})")