import streamlit as st
import pandas as pd
import joblib
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Crypto Price Predictor",
    page_icon="🚀",
    layout="wide"
)

# --- Load Model ---
@st.cache_resource
def load_model():
    """Loads the trained prediction model from file."""
    model_path = 'price_prediction_model.joblib'
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return model
    return None

model = load_model()

# --- UI Elements ---
st.title("Crypto Price Prediction Dashboard 📈")
st.write(
    "This app uses a machine learning model to predict the next hour's "
    "cryptocurrency price based on recent market and social media data."
)

if model is None:
    st.error(
        "Model file not found! Please run `train_model.py` first to create "
        "`price_prediction_model.joblib`."
    )
else:
    st.header("Make a Prediction")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        last_hour_close = st.number_input(
            "Last Hour's Closing Price ($)", 
            min_value=0.0, 
            value=60000.0, 
            step=100.0,
            help="Enter the closing price from the previous hour."
        )
    
    with col2:
        volume = st.number_input(
            "Current Hour's Trading Volume", 
            min_value=0.0, 
            value=1500.0, 
            step=50.0,
            help="Enter the total trading volume for the current hour."
        )

    with col3:
        post_count = st.slider(
            "Current Hour's Social Media Post Count", 
            min_value=0, 
            max_value=1000, 
            value=100,
            help="Estimate the number of relevant posts on Twitter and Reddit this hour."
        )

    # Predict button
    if st.button("Predict Next Hour's Price", type="primary"):
        # Create a DataFrame from the inputs
        features = pd.DataFrame([[post_count, volume, last_hour_close]], 
                                columns=['feature_post_count', 'feature_volume', 'feature_last_hour_close'])
        
        # Make prediction
        prediction = model.predict(features)
        
        # Display result
        st.success(f"Predicted Price for the Next Hour: **${prediction[0]:,.2f}**")

st.sidebar.header("About This Project")
st.sidebar.info(
    "This dashboard is the final piece of a full data pipeline project. It leverages data scraped "
    "from Twitter and Reddit, combined with market data from Binance, to power a predictive model."
)
#streamlit run dashboard.py