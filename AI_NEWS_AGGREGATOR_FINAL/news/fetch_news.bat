@echo off
cd E:\ai_news_aggregator
call env\Scripts\activate
python manage.py fetch_news
