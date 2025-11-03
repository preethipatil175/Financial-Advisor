import numpy as np
import pandas as pd
import pickle
import os
from dotenv import load_dotenv
import warnings

# Load environment variables
load_dotenv()

warnings.filterwarnings('ignore', message='X does not have valid feature names')

# Load models and preprocessor
try:
    Jmodel = pickle.load(open('jmodel.pkl', 'rb'))
    Wmodel = pickle.load(open('wmodel.pkl', 'rb'))
    Cmodel = pickle.load(open('cmodel.pkl', 'rb'))
    Smodel = pickle.load(open('smodel.pkl', 'rb'))
    Bmodel = pickle.load(open('bmodel.pkl', 'rb'))
    preprocessor = pickle.load(open('preprocessor.pkl', 'rb'))
except FileNotFoundError as e:
    raise RuntimeError(f"Model file missing: {e}")

# Commodity models and MSP info
commodity_info = {
    "jowar":     {"model": Jmodel, "min_msp": 1550, "max_msp": 2970},
    "wheat":     {"model": Wmodel, "min_msp": 1350, "max_msp": 2125},
    "cotton":    {"model": Cmodel, "min_msp": 3600, "max_msp": 6080},
    "sugarcane": {"model": Smodel, "min_msp": 2250, "max_msp": 2775},
    "bajara":    {"model": Bmodel, "min_msp": 1175, "max_msp": 2350}
}

month_names_en = ["", "January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]

month_names_kn = ["", "ಜನವರಿ", "ಫೆಬ್ರವರಿ", "ಮಾರ್ಚ್", "ಏಪ್ರಿಲ್", "ಮೇ", "ಜೂನ್",
                  "ಜುಲೈ", "ಆಗಸ್ಟ್", "ಸೆಪ್ಟೆಂಬರ್", "ಅಕ್ಟೋಬರ್", "ನವೆಂಬರ್", "ಡಿಸೆಂಬರ್"]

def predict_crop_price(commodity, month, year, rainfall, language="en"):
    if commodity not in commodity_info:
        return {"error": "Invalid commodity"}

    if not (1 <= int(month) <= 12):
        return {"error": "Invalid month"}

    try:
        year = int(year)
        rainfall = float(rainfall)
    except ValueError:
        return {"error": "Invalid input types"}

    try:
        features_df = pd.DataFrame([[month, year, rainfall]], columns=['Month', 'Year', 'Rainfall'])
        transformed = preprocessor.transform(features_df)

        model = commodity_info[commodity]["model"]
        min_msp = commodity_info[commodity]["min_msp"]
        max_msp = commodity_info[commodity]["max_msp"]

        prediction = model.predict(transformed).reshape(1, -1)
        predicted_index = round(prediction[0][0], 3)

        min_price = round((predicted_index * min_msp) / 100, 2)
        max_price = round((predicted_index * max_msp) / 100, 2)
        avg_price = round((min_price + max_price) / 2, 2)

        response = {
            "commodity": commodity,
            "month": month_names_en[month] if language == "en" else month_names_kn[month],
            "month_num": month,
            "year": year,
            "rainfall_mm": rainfall,
            "predicted_index": predicted_index,
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": avg_price,
            "message": "Prediction successful" if language == "en" else "ಅಂದಾಜು ಯಶಸ್ವಿಯಾಗಿದೆ"
        }

        return response

    except Exception as e:
        return {"error": str(e)}