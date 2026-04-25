import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# dataset
X = np.array([
    [2,1,0.2,800],
    [3,2,0.3,1200],
    [4,3,0.5,2000],
    [5,4,1.0,3000]
])

y = np.array([150000, 250000, 450000, 800000])

model = RandomForestRegressor()
model.fit(X, y)

# SAVE DIRECTLY INTO BACKEND
joblib.dump(model, "backend/model.pkl")

print("MODEL CREATED")