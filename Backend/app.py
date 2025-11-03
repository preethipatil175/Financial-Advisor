import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from flask import Flask, request, jsonify,render_template
from advisor import get_financial_advice
from kannadacrop import predict_crop_price
from exp_budget import FarmerExpenseTracker
# from loan_recommender import recommend_loan
import joblib
# import numpy as np

app = Flask(__name__)

# Initialize expense tracker
tracker = FarmerExpenseTracker()

# model = joblib.load('loan_recommender.pkl')
# le_crop = joblib.load('le_crop.pkl')
# le_loan = joblib.load('le_loan.pkl')
# le_land = joblib.load('le_land.pkl')
# le_location = joblib.load('le_location.pkl')

#loan-recommendation Route
@app.route('/loan-recommender', methods=['POST'])
def loan_recommend_route():
    data = request.json
    land_type = data.get('LandType')
    land_size = float(data.get('LandSize'))
    location = data.get('Location')
    crop = data.get('CropType')
    income = int(data.get('Income'))

    # ✅ Call your function from loan_recommender.py
    result = get_loan_recommendation(land_type, land_size, location, crop, income)

    return jsonify(result)

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Farmer Assistant API"}), 200

# --- Financial Advisor Route ---
@app.route('/financial-advice', methods=['POST'])
def financial_advice():
    data = request.json
    risk = data.get('risk_profile')
    term = data.get('investment_term')
    initial = data.get('initial_amount')
    monthly = data.get('monthly_saving')

    advice = get_financial_advice(risk, term, initial, monthly)
    return jsonify(advice)

# --- Crop Price Prediction Route ---
@app.route('/predict-price', methods=['POST'])
def predict_price():
    data = request.json
    crop = data.get('crop')
    month = int(data.get('month'))
    year = int(data.get('year'))
    rainfall = float(data.get('rainfall'))
    lang = data.get('language', 'en')  # Optional, default to English

    predicted_price = predict_crop_price(crop, month, year, rainfall, language=lang)
    return jsonify(predicted_price)

# --- Expense and Budget Tracker Route ---
@app.route('/update-expense', methods=['POST'])
def update_exp():
    data = request.json
    name = data['name']
    category = data['category']
    amount = data['amount']
    date = data.get('date')  # Optional

    result = tracker.add_expense(name, category, amount, date)
    return jsonify(result)

@app.route('/budget-status', methods=['GET'])
def budget_status():
    budget = tracker.get_budget()
    status = tracker.get_summary(budget)
    return jsonify(status)

# Optional: Set budget route
@app.route('/set-budget', methods=['POST'])
def set_budget():
    data = request.json
    amount = data.get('amount')
    result = tracker.set_budget(amount)
    return jsonify(result)

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)


