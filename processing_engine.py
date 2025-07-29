import pandas as pd
import psycopg2
from binance.client import Client
import os
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

def fetch_social_data_from_db(conn):
    """Fetches and combines Twitter and Reddit data from the database."""
    print("Fetching social media data from PostgreSQL...")
    twitter_df = pd.read_sql("SELECT created_at, text FROM twitter_posts", conn)
    twitter_df['source'] = 'twitter'
    
    reddit_df = pd.read_sql("SELECT created_utc AS created_at, title AS text FROM reddit_posts", conn)
    reddit_df['source'] = 'reddit'
    
    social_df = pd.concat([twitter_df, reddit_df], ignore_index=True)
    social_df['created_at'] = pd.to_datetime(social_df['created_at'], utc=True)
    social_df = social_df.set_index('created_at').sort_index()
    
    print(f"Found {len(social_df)} total social media posts.")
    return social_df

def fetch_market_data(symbol, start_date_str):
    """Fetches historical market data from Binance."""
    print(f"Fetching market data for {symbol} from Binance...")
    binance_client = Client() # Public data doesn't require an API key
    
    klines = binance_client.get_historical_klines(
        symbol, Client.KLINE_INTERVAL_1HOUR, start_date_str
    )
    
    market_df = pd.DataFrame(klines, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
        'taker_buy_quote_asset_volume', 'ignore'
    ])
    
    market_df['open_time'] = pd.to_datetime(market_df['open_time'], unit='ms', utc=True)
    market_df = market_df[['open_time', 'open', 'high', 'low', 'close', 'volume']].set_index('open_time')
    market_df = market_df.astype(float)
    
    print(f"Found {len(market_df)} hourly market data records for {symbol}.")
    return market_df

def main():
    parser = argparse.ArgumentParser(description="Processing Engine for social and market data.")
    parser.add_argument("symbol", help="The crypto symbol to fetch (e.g., BTCUSDT).")
    parser.add_argument("start_date", help="The start date for market data (YYYY-MM-DD).")
    args = parser.parse_args()

    conn = get_db_connection()
    if not conn:
        return
        
    social_df = fetch_social_data_from_db(conn)
    market_df = fetch_market_data(args.symbol, args.start_date)
    conn.close()

    social_agg_df = social_df.resample('H').size().to_frame('post_count')
    combined_df = market_df.join(social_agg_df, how='left').fillna(0)
    
    filename = f"processed_{args.symbol}_data.csv"
    combined_df.to_csv(filename)
    print(f"\nSuccessfully created combined dataset: {filename}")

if __name__ == "__main__":
    main()