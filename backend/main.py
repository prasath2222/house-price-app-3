from fastapi import FastAPI
import numpy as np
import joblib

app = FastAPI()

model = joblib.load("model.pkl")

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/predict")
def predict(data: dict):

    X = np.array([[
        data["bedrooms"],
        data["bathrooms"],
        data["acre"],
        data["size"]
    ]])

    price = model.predict(X)[0]

    return {"price": float(price)}