from dotenv import load_dotenv
load_dotenv()
import requests
from django.core.management.base import BaseCommand
from news.models import News
from datetime import datetime
import openai
import os  # Import os to access environment variables

# Use environment variables for sensitive keys
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')

class Command(BaseCommand):
    help = 'Fetch news from NewsAPI and save to database'

    def handle(self, *args, **kwargs):
        url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=10&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        data = response.json()

        for article in data.get('articles', []):
            title = article['title']
            content = article.get('content') or article.get('description') or ''
            url_link = article['url']
            published_at = article['publishedAt']
            category = article.get('category', 'Technology')

            if News.objects.filter(title=title).exists():
                continue

            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You summarize news articles."},
                        {"role": "user", "content": content}
                    ],
                    max_tokens=100
                )
                summary = completion.choices[0].message['content']
            except Exception:
                summary = content[:150] + '...'

            News.objects.create(
                title=title,
                summary=summary,
                url=url_link,
                category=category,
                published_at=datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
            )

        self.stdout.write(self.style.SUCCESS('News fetched and saved.'))
