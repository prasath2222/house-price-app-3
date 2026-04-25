import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="House Price Predictor PRO", layout="centered")

# ---------------- BACKEND URL ----------------
BASE_URL = "https://house-price-app-3-y2t9.onrender.com"

# ---------------- SESSION ----------------
if "price" not in st.session_state:
    st.session_state.price = None

# ---------------- CHECK BACKEND ----------------
try:
    res = requests.get(BASE_URL)
    if res.status_code == 200:
        st.success("Backend Connected")
    else:
        st.error("Backend Not Running")
except:
    st.error("Backend Not Running")

# ---------------- UI ----------------
st.title("🏡 House Price Predictor PRO")

col1, col2 = st.columns(2)

with col1:
    bedrooms = st.slider("Bedrooms", 1, 10, 2)
    bathrooms = st.slider("Bathrooms", 1, 10, 2)

with col2:
    acre = st.slider("Acre Lot", 0.1, 2.0, 0.5)
    size = st.slider("House Size (sqft)", 300, 5000, 1200)

# ---------------- PREDICT ----------------
if st.button("🚀 Predict Price"):

    data = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "acre": acre,
        "size": size
    }

    try:
        res = requests.post(f"{BASE_URL}/predict", json=data)

        if res.status_code == 200:
            price = res.json()["price"]
            st.session_state.price = price
        else:
            st.error("Prediction failed")

    except:
        st.error("Cannot connect to backend")

# ---------------- RESULT ----------------
if st.session_state.price is not None:

    price = st.session_state.price
    low = price * 0.9
    high = price * 1.1

    st.markdown(f"### 💰 ${price:,.2f}")
    st.markdown(f"Range: ${low:,.0f} - ${high:,.0f}")

    avg = 350000
    if price < avg * 0.8:
        st.success("Undervalued")
    elif price > avg * 1.2:
        st.error("Overpriced")
    else:
        st.info("Fair Price")

    # ---------------- GRAPH ----------------
    st.markdown("### 📈 Future Trend")

    years = [1,2,3,4,5]
    growth = 0.06
    future_prices = [price * (1 + growth)**y for y in years]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years,
        y=future_prices,
        mode='lines+markers'
    ))

    st.plotly_chart(fig, use_container_width=True)