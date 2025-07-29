import requests
import os
import json
import pandas as pd
import argparse 
import praw # Import PRAW

# --- Twitter Functions ---

def scrape_twitter(query):
    """Handles the entire process of scraping Twitter."""
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        print("ERROR: TWITTER_BEARER_TOKEN not set.")
        return

    headers = {"Authorization": f"Bearer {bearer_token}"}
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        'query': query,
        'tweet.fields': "created_at,author_id,public_metrics",
        'max_results': 100
    }
    
    print(f"--> Searching Twitter for: '{query}'")
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Twitter API Error: {response.status_code} {response.text}")
        return
    
    json_response = response.json()
    if 'data' in json_response:
        tweets = json_response['data']
        processed_tweets = [
            {
                'id': t['id'], 'author_id': t['author_id'], 'created_at': t['created_at'],
                'text': t['text'], 'likes': t['public_metrics']['like_count'],
                'retweets': t['public_metrics']['retweet_count']
            } for t in tweets
        ]
        df = pd.DataFrame(processed_tweets)
        filename = query.replace(" ", "_") + "_twitter.csv"
        df.to_csv(filename, index=False)
        print(f"--> Successfully saved {len(df)} tweets to {filename}")
    else:
        print("No tweets found on Twitter for this query.")

# --- Reddit Functions ---

def scrape_reddit(subreddit_name):
    """Handles the entire process of scraping a subreddit."""
    try:
        reddit = praw.Reddit(
            client_id=os.environ.get("REDDIT_CLIENT_ID"),
            client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
            user_agent=f"script:MyScraper:v1.0 (by /u/{os.environ.get('REDDIT_USERNAME')})",
            username=os.environ.get("REDDIT_USERNAME"),
            password=os.environ.get("REDDIT_PASSWORD"),
            check_for_async=False # Add this line to avoid a common warning
        )
        print(f"--> Authenticated with Reddit as /u/{reddit.user.me()}")
    except Exception as e:
        print(f"ERROR: Could not connect to Reddit. Check your credentials. Details: {e}")
        return

    print(f"--> Scraping top 100 posts from subreddit: r/{subreddit_name}")
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.hot(limit=100):
        posts.append({
            'id': post.id,
            'title': post.title,
            'score': post.score,
            'url': post.url,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc
        })

    if posts:
        df = pd.DataFrame(posts)
        filename = subreddit_name + "_reddit.csv"
        df.to_csv(filename, index=False)
        print(f"--> Successfully saved {len(df)} posts to {filename}")
    else:
        print(f"Could not find any posts in r/{subreddit_name}.")

# --- Main Execution ---

def main():
    parser = argparse.ArgumentParser(description="Scrape data from Twitter or Reddit.")
    parser.add_argument("platform", help="The platform to scrape: 'twitter' or 'reddit'")
    parser.add_argument("query", help="Twitter search query OR a single subreddit name for Reddit")
    args = parser.parse_args()

    if args.platform.lower() == 'twitter':
        scrape_twitter(args.query)
    elif args.platform.lower() == 'reddit':
        scrape_reddit(args.query)
    else:
        print("Invalid platform. Please choose 'twitter' or 'reddit'.")

if __name__ == "__main__":
    main()