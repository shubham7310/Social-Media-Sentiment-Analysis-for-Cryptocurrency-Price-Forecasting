Social-Media-Sentiment-Analysis-for-Cryptocurrency-Price-Forecasting
This project is an end-to-end data pipeline that scrapes social media data from Twitter and Reddit, combines it with live market data from the Binance API, and uses a machine learning model to predict cryptocurrency price movements. The final prediction is displayed on an interactive Streamlit dashboard.

Project Architecture
The pipeline is structured into five distinct phases, from data collection to a live user interface.

Features
Multi-Platform Data Scraping: Gathers real-time data from both Twitter (X API) and Reddit (PRAW).

Persistent Data Storage: Uses a PostgreSQL database to store and manage raw scraped data efficiently.

Data Enrichment: Combines social media metrics with live cryptocurrency market data (price, volume) from the Binance API.

Machine Learning Model: Trains a Linear Regression model to forecast the next hour's price.

Interactive Dashboard: Deploys the model in a user-friendly Streamlit web application for live predictions.

Technologies Used
Language: Python 3

Database: PostgreSQL

APIs: Twitter API v2, Reddit API (PRAW), Binance API

Data Science & ML:

pandas for data manipulation

scikit-learn for machine learning

matplotlib & seaborn for data visualization

Web Dashboard: streamlit

Database Connector: psycopg2-binary

Setup and Installation
Follow these steps to set up the project locally.

1. Prerequisites
Python 3.8+

PostgreSQL server installed and running.

2. Clone the Repository
git clone https://github.com/shubham7310/Social-Media-Sentiment-Analysis-for-Cryptocurrency-Price-Forecasting.git
cd Social-Media-Sentiment-Analysis-for-Cryptocurrency-Price-Forecasting

3. Set Up Virtual Environment & Install Dependencies
It's recommended to use a virtual environment.

# Create and activate the virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install required packages
pip install -r requirements.txt

(You will need to create a requirements.txt file by running pip freeze > requirements.txt)

4. Set Up the Database
Create a new PostgreSQL database.

Create the twitter_posts and reddit_posts tables using the SQL commands found in the project documentation or scripts.

5. Configure Environment Variables
This project uses environment variables to securely manage API keys and database credentials. Set the following variables in your terminal session:

# For PowerShell
$env:TWITTER_BEARER_TOKEN="YOUR_TWITTER_TOKEN"
$env:REDDIT_CLIENT_ID="YOUR_REDDIT_ID"
$env:REDDIT_CLIENT_SECRET="YOUR_REDDIT_SECRET"
$env:REDDIT_USERNAME="YOUR_REDDIT_USERNAME"
$env:REDDIT_PASSWORD="YOUR_REDDIT_PASSWORD"

$env:DB_HOST="localhost"
$env:DB_NAME="your_db_name"
$env:DB_USER="your_db_user"
$env:DB_PASS="your_db_password"
$env:PGCLIENTENCODING="UTF8" # Important for handling special characters

How to Run the Pipeline
Execute the scripts in the following order:

1. Scrape Data:
Collect data from Twitter and Reddit.

python scrapers.py twitter "Your Query"
python scrapers.py reddit YourSubreddit

2. Load Data to Database:
Load the generated CSV files into PostgreSQL.

python load_to_db.py twitter your_twitter_file.csv
python load_to_db.py reddit your_reddit_file.csv

3. Run the Processing Engine:
Combine social and market data.

python processing_engine.py BTCUSDT "YYYY-MM-DD"

4. Train the Model:
Train and save the prediction model.

python train_model.py processed_BTCUSDT_data.csv

5. Launch the Dashboard:
Start the interactive Streamlit application.

streamlit run dashboard.py
