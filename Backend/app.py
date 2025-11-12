from flask import Flask, request, jsonify, render_template
from advisor import get_financial_advice
from kannadacrop import predict_crop_price
from exp_budget import FarmerExpenseTracker
from loan_recommender import get_loan_recommendation
import crop_price  # ✅ Import your functions
import numpy as np


app = Flask(__name__)

# Initialize expense tracker
tracker = FarmerExpenseTracker()


# ✅ FRONTEND HOME PAGE
@app.route('/')
def homepage():
    return render_template("home.html")


# ✅ API Home (optional)
@app.route('/api')
def api_home():
    return jsonify({"message": "Welcome to the Farmer Assistant API"}), 200


# ======================================================================
# ✅ FINANCIAL ADVISOR
# ======================================================================

# Backend
@app.route('/financial-advice', methods=['POST'])
def financial_advice():
    data = request.json
    risk = data.get('risk_profile')
    term = data.get('investment_term')
    initial = data.get('initial_amount')
    monthly = data.get('monthly_saving')

    advice = get_financial_advice(risk, term, initial, monthly)
    return jsonify(advice)

# Frontend
@app.route('/financial-advice-page')
def financial_advice_page():
    return render_template("financial_advice.html")


# ======================================================================
# ✅ CROP PRICE PREDICTION
# ======================================================================

# # Backend
# @app.route('/predict-price', methods=['POST'])
# def predict_price():
#     data = request.json
#     crop = data.get('crop')
#     month = int(data.get('month'))
#     year = int(data.get('year'))
#     rainfall = float(data.get('rainfall'))
#     lang = data.get('language', 'en')
    
#     if crop not in commodity_info:
#         return jsonify({'error': 'Invalid crop name'})
    
#     predicted_index, min_price, max_price, avg_price = model_predict(crop, month, year, rainfall)

#     # ✅ Generate smooth graph data for visualization (dynamic)
#     months = np.arange(1, 13)
#     graph_data = []
#     for m in months:
#         _, _, _, avg = model_predict(crop, m, year, rainfall)
#         graph_data.append({"month": m, "avg_price": avg})

#     return jsonify({
#         "crop": crop.capitalize(),
#         "month": month,
#         "year": year,
#         "rainfall": rainfall,
#         "min_price": min_price,
#         "max_price": max_price,
#         "avg_price": avg_price,
#         "graph_data": graph_data
#     })

# # Frontend form
# @app.route('/price-form')
# def price_form():
#     return render_template("crop_prediction.html")

# @app.route("/get-price", methods=["POST"])
# def get_price_html():
#     crop = request.form.get("crop").lower()
#     month = int(request.form.get("month"))
#     year = int(request.form.get("year"))
#     rainfall = float(request.form.get("rainfall"))
#     lang = request.form.get("language", "en")

#     # ✅ Predict using the imported model
#     predicted_index, min_price, max_price, avg_price = model_predict(crop, month, year, rainfall)

#     # ✅ Prepare graph data for smooth chart animation
#     months = np.arange(1, 13)
#     graph_data = []
#     for m in months:
#         _, _, _, avg = model_predict(crop, m, year, rainfall)
#         graph_data.append({"month": m, "avg_price": avg})

#     # ✅ Pass results to HTML
#     result = {
#         "crop": crop.capitalize(),
#         "month": month,
#         "year": year,
#         "rainfall": rainfall,
#         "min_price": min_price,
#         "max_price": max_price,
#         "avg_price": avg_price,
#         "graph_data": graph_data
#     }

#     return render_template(
#         "crop_prediction.html",
#         result=result
#     )


# ==============================================================
# ✅ BACKEND - Predict Price API
# ==============================================================
@app.route('/predict-price', methods=['POST'])
def predict_price_route():
    try:
        data = request.json
        crop = data.get('crop').lower()
        month = int(data.get('month'))
        year = int(data.get('year'))
        rainfall = float(data.get('rainfall'))

        # ✅ Validate crop
        if crop not in crop_price.commodity_info:
            return jsonify({'error': f'Invalid crop name: {crop}'}), 400

        # ✅ Predict using crop_price.py function
        predicted_index, min_price, max_price, avg_price = crop_price.predict_price(
            crop, month, year, rainfall
        )

        # ✅ Generate smooth dynamic graph data (for each month)
        months = np.arange(1, 13)
        graph_data = []
        for m in months:
            _, _, _, avg = crop_price.predict_price(crop, m, year, rainfall)
            graph_data.append({"month": int(m), "avg_price": float(avg)})

        return jsonify({
            "crop": crop.capitalize(),
            "month": month,
            "year": year,
            "rainfall": rainfall,
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": avg_price,
            "graph_data": graph_data
        })

    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


# ==============================================================
# ✅ FRONTEND FORM - HTML Page Rendering
# ==============================================================
@app.route('/price-form')
def price_form():
    return render_template("crop_prediction.html")


# ==============================================================
# ✅ FORM SUBMISSION (for HTML)
# ==============================================================
@app.route("/get-price", methods=["POST"])
def get_price_html():
    try:
        crop = request.form.get("crop").lower()
        month = int(request.form.get("month"))
        year = int(request.form.get("year"))
        rainfall = float(request.form.get("rainfall"))

        # ✅ Predict using the imported function
        predicted_index, min_price, max_price, avg_price = crop_price.predict_price(
            crop, month, year, rainfall
        )

        # ✅ Prepare graph data for smooth chart animation
        months = np.arange(1, 13)
        graph_data = []
        for m in months:
            _, _, _, avg = crop_price.predict_price(crop, m, year, rainfall)
            graph_data.append({"month": int(m), "avg_price": float(avg)})

        # ✅ Pass results to HTML
        result = {
            "crop": crop.capitalize(),
            "month": month,
            "year": year,
            "rainfall": rainfall,
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": avg_price,
            "graph_data": graph_data
        }

        return render_template(
            "crop_prediction.html",
            result=result
        )

    except Exception as e:
        import traceback
        return render_template(
            "crop_prediction.html",
            error=str(e),
            trace=traceback.format_exc()
        )



# ======================================================================
# ✅ EXPENSE TRACKER
# ======================================================================

# Backend add expense
@app.route('/update-expense', methods=['POST'])
def update_exp():
    data = request.json
    name = data['name']
    category = data['category']
    amount = data['amount']
    date = data.get('date')

    result = tracker.add_expense(name, category, amount, date)
    return jsonify(result)

# Frontend - add expense
@app.route('/expense-form')
def expense_form():
    categories = tracker.get_categories()
    return render_template("add_expense.html", categories=categories)

@app.route('/add-expense-page', methods=['POST'])
def add_expense_html():
    name = request.form.get('name')
    category = request.form.get('category')
    amount = request.form.get('amount')
    date = request.form.get('date')

    result = tracker.add_expense(name, category, amount, date)
    categories = tracker.get_categories()

    return render_template("add_expense.html", categories=categories, result=result)

# Backend budget summary
@app.route('/budget-status', methods=['GET'])
def budget_status():
    budget = tracker.get_budget()
    status = tracker.get_summary(budget)
    return jsonify(status)

# Frontend budget summary
@app.route('/budget-summary-page')
def budget_summary_html():
    budget = tracker.get_budget()
    summary = tracker.get_summary(budget)
    return render_template("budget_summary.html", summary=summary)


# ======================================================================
# ✅ LOAN RECOMMENDER
# ======================================================================

# Backend
@app.route('/loan-recommender', methods=['POST'])
def loan_recommend_route():
    data = request.json
    land_type = data.get('LandType')
    land_size = float(data.get('LandSize'))
    location = data.get('Location')
    crop = data.get('CropType')
    income = int(data.get('Income'))

    result = get_loan_recommendation(land_type, land_size, location, crop, income)
    return jsonify(result)


if __name__ == '__main__':
    print("✅ Starting Flask server...")
    app.run(debug=True)
