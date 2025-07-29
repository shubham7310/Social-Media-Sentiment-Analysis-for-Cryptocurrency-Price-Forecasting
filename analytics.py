import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os

def analyze_data(filepath):
    """
    Loads processed data and performs analysis, generating plots and stats.
    """
    print(f"Loading processed data from {filepath}...")
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return

    df = pd.read_csv(filepath, index_col='open_time', parse_dates=True)
    
    # --- 1. Time Series Visualization ---
    print("Generating Time Series plot of Price vs. Post Count...")
    fig, ax1 = plt.subplots(figsize=(15, 7))

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Closing Price (USD)', color='blue')
    ax1.plot(df.index, df['close'], color='blue', label='Closing Price')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Social Media Post Count', color='red')
    ax2.bar(df.index, df['post_count'], color='red', alpha=0.5, label='Post Count', width=0.02)
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title('Crypto Price vs. Social Media Activity')
    fig.tight_layout()
    plt.savefig('price_vs_posts_timeseries.png')
    print("Saved plot to price_vs_posts_timeseries.png")
    plt.close()

    # --- 2. Correlation Analysis ---
    print("\nCalculating correlations...")
    df['price_change'] = df['close'].diff()
    
    correlation_df = df[['close', 'volume', 'post_count', 'price_change']].corr()
    
    print("Correlation Matrix:")
    print(correlation_df)
    
    # --- 3. Scatter Plot ---
    print("\nGenerating Scatter plot of Post Count vs. Price Change...")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='post_count', y='price_change')
    plt.title('Hourly Post Count vs. Hourly Price Change')
    plt.xlabel('Number of Social Media Posts')
    plt.ylabel('Change in Closing Price (USD)')
    plt.grid(True)
    plt.savefig('posts_vs_price_change_scatter.png')
    print("Saved plot to posts_vs_price_change_scatter.png")
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Analyze processed crypto and social media data.")
    parser.add_argument("filepath", help="Path to the processed CSV file (e.g., processed_BTCUSDT_data.csv).")
    args = parser.parse_args()
    analyze_data(args.filepath)

if __name__ == "__main__":
    main()