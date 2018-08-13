#!/usr/bin/python python2.7

import psycopg2

def query_news(query):
    """Run queries on news database and return query results"""
    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results

def show_popular_articles():
    """Print top three articles of all time"""
    popular_articles_query = """
    select articles.title, count(*) from articles, log
    where log.status = '200 OK' and articles.slug = substr(log.path, 10)
    group by articles.title
    order by count desc limit 3;
    """
    results = query_news(popular_articles_query)
    print("1. What are the most popular three articles of all time?")
    for result in results:
        print("{} -- {} views".format(result[0], result[1]))

def show_popular_authors():
    """Print all authors by popularity"""
    popular_authors_query = """
    select title_author.name, sum(article_views.count) from title_author
    join article_views on (title_author.title = article_views.title)
    group by title_author.name order by sum desc;
    """
    results = query_news(popular_authors_query)
    print("2. Who are the most popular article authors of all time?")
    for result in results:
        print("{} -- {} views".format(result[0], result[1]))

def show_error_days():
    error_days_query = """
    select total_requests.date,
    round(error_requests.request_num::NUMERIC / total_requests.request_num * 100, 1) as errors
    from total_requests, error_requests
    where total_requests.date = error_requests.date and
    round(error_requests.request_num::NUMERIC / total_requests.request_num * 100, 1) > 1.0
    group by total_requests.date, errors;
    """
    results = query_news(error_days_query)    
    print("3. On which days did more than 1% of requests lead to errors?")
    for result in results:
        print("{} -- {}% errors".format(result[0], result[1]))

show_popular_articles()
show_popular_authors()
show_error_days()
