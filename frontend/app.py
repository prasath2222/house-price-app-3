import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="House Price Predictor PRO", layout="centered")

# ---------------- SESSION ----------------
if "price" not in st.session_state:
    st.session_state.price = None

# ---------------- BACKEND CHECK ----------------
try:
    requests.get("http://127.0.0.1:8000/docs")
    st.success("Backend Connected")
except:
    st.error("Backend Not Running")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.block-container {
    max-width: 750px;
    padding-top: 1rem;
}
header {visibility: hidden;}
.title {
    text-align:center;
    font-size:30px;
    font-weight:700;
}
.sub {
    text-align:center;
    color:gray;
    margin-bottom:20px;
}
.result {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    padding:12px;
    border-radius:8px;
    text-align:center;
    font-size:20px;
    font-weight:bold;
}
.range {
    text-align:center;
    color:#9ca3af;
    margin-top:5px;
}
.stButton>button {
    width:100%;
    border-radius:8px;
    height:40px;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='title'>🏡 House Price Predictor PRO</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>FastAPI + Streamlit Connected</div>", unsafe_allow_html=True)

st.divider()

# ---------------- INPUT ----------------
col1, col2 = st.columns(2)

with col1:
    bedrooms = st.slider("Bedrooms", 1, 10, 2)
    bathrooms = st.slider("Bathrooms", 1, 10, 2)

with col2:
    acre = st.slider("Acre Lot", 0.1, 2.0, 0.5)
    size = st.slider("House Size (sqft)", 300, 5000, 1200)

# ---------------- BUTTON ----------------
if st.button("🚀 Predict Price"):

    with st.spinner("Predicting..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={
                    "bedrooms": bedrooms,
                    "bathrooms": bathrooms,
                    "size": size,
                    "acre": acre,
                    "lat": 12.97,
                    "lon": 77.59
                }
            )

            if response.status_code == 200:
                st.session_state.price = response.json()["price"]
            else:
                st.error("Backend error")

        except Exception as e:
            st.error(f"Connection error: {e}")

# ---------------- RESULT ----------------
if st.session_state.price is not None:

    price = st.session_state.price
    low = price * 0.9
    high = price * 1.1

    st.markdown(f"<div class='result'>💰 ${price:,.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='range'>Range: ${low:,.0f} - ${high:,.0f}</div>", unsafe_allow_html=True)

    avg = 350000
    if price < avg * 0.8:
        st.success("Undervalued")
    elif price > avg * 1.2:
        st.error("Overpriced")
    else:
        st.info("Fair Price")

    st.divider()

    # ---------------- GRAPH ----------------
    st.markdown("### 📈 Future Trend")

    years = [1,2,3,4,5]
    growth = 0.06
    future_prices = [price * (1 + growth)**y for y in years]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=future_prices, mode='lines+markers'))
    fig.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=0))

    st.plotly_chart(fig, use_container_width=True)