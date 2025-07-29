import os
import psycopg2
import pandas as pd
import argparse

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS")
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def load_twitter_data(conn, filepath):
    """Loads Twitter data from a CSV file into the database."""
    print(f"Loading Twitter data from {filepath}...")
    df = pd.read_csv(filepath)
    cursor = conn.cursor()
    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO twitter_posts (id, author_id, created_at, text, likes, retweets)
            VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
            """,
            (row['id'], row['author_id'], row['created_at'], row['text'], row['likes'], row['retweets'])
        )
    conn.commit()
    cursor.close()
    print(f"Successfully processed {len(df)} records for twitter_posts.")

def load_reddit_data(conn, filepath):
    """Loads Reddit data from a CSV file into the database."""
    print(f"Loading Reddit data from {filepath}...")
    df = pd.read_csv(filepath)
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    cursor = conn.cursor()
    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO reddit_posts (id, title, score, url, num_comments, created_utc)
            VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
            """,
            (row['id'], row['title'], row['score'], row['url'], row['num_comments'], row['created_utc'])
        )
    conn.commit()
    cursor.close()
    print(f"Successfully processed {len(df)} records for reddit_posts.")

def main():
    parser = argparse.ArgumentParser(description="Load data from CSV into PostgreSQL.")
    parser.add_argument("platform", choices=['twitter', 'reddit'], help="Platform data to load.")
    parser.add_argument("filepath", help="Path to the CSV file.")
    args = parser.parse_args()

    conn = get_db_connection()
    if conn:
        if args.platform == 'twitter':
            load_twitter_data(conn, args.filepath)
        elif args.platform == 'reddit':
            load_reddit_data(conn, args.filepath)
        conn.close()

if __name__ == "__main__":
    main()