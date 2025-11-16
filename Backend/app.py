from flask import Flask, request, jsonify, render_template,redirect
from advisor import get_financial_advice
from kannadacrop import predict_crop_price
from exp_budget import FarmerExpenseTracker
from loan_system import get_loan_recommendation
from crop_price import predict_price


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

def get_financial_advice(risk, term, initial, monthly):
    # Handle empty or missing values gracefully
    risk = risk or "Not specified"
    term = term or "Not specified"
    initial = initial or 0
    monthly = monthly or 0

    # Simple static logic (replace later with real calculations)
    if risk == "conservative":
        suggestion = "Focus on safe investments like Fixed Deposits or Government Bonds."
    elif risk == "moderate":
        suggestion = "Diversify between Mutual Funds, Gold, and Low-risk Stocks."
    elif risk == "aggressive":
        suggestion = "Invest more in Equities, Startups, and High-growth Mutual Funds."
    else:
        suggestion = "Please select a valid risk profile for better recommendations."

    return {
        "Risk Profile": risk,
        "Investment Term": term,
        "Initial Amount": f"₹{initial}",
        "Monthly Saving": f"₹{monthly}",
        "Advisor Suggestion": suggestion
    }


# ✅ Backend route (handles JSON properly)
@app.route('/financial-advice', methods=['POST'])
def financial_advice():
    try:
        data = request.get_json(force=True)  # ensures JSON parsing works even if headers are missing
    except Exception:
        return jsonify({"error": "Invalid JSON received"}), 400

    risk = data.get('risk_profile')
    term = data.get('investment_term')
    initial = data.get('initial_amount')
    monthly = data.get('monthly_saving')

    advice = get_financial_advice(risk, term, initial, monthly)
    return jsonify(advice)


# ✅ Frontend route (renders your HTML page)
@app.route('/financial-advice-page')
def financial_advice_page():
    return render_template("financial_advice.html")


# ======================================================================
# ✅ CROP PRICE PREDICTION
# ======================================================================

# # # Backend
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


# Frontend
@app.route('/price-form')
def price_form():
    return render_template("crop_prediction.html")

@app.route('/predict-price', methods=['POST'])
def predict_price_api():
    try:
        data = request.json
        crop = data.get('crop')
        month = int(data.get('month'))
        year = int(data.get('year'))
        rainfall = float(data.get('rainfall'))

        # Call your ML prediction function
        _, min_price, max_price, avg_price = predict_price(crop, month, year, rainfall)

        return jsonify({
            "crop": crop.capitalize(),
            "month": month,
            "year": year,
            "rainfall": rainfall,
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": avg_price
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400



# ======================================================================
# ✅ EXPENSE TRACKER
# ======================================================================

def get_recent_expenses():
    try:
        with open("expenses.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        expenses = []
        for line in reversed(lines[-5:]):  # show last 5
            parts = line.strip().split(",")
            if len(parts) != 4:
                print("⚠️ Skipping bad line:", line.strip())  # Debug info
                continue

            name, category, amount, date = parts
            expenses.append({
                "name": name,
                "category": category,
                "amount": amount,
                "date": date
            })
        return expenses
    except FileNotFoundError:
        return []


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
    recent_expenses = get_recent_expenses()
    return render_template("add_expense.html", categories=categories,recent_expenses=recent_expenses)

@app.route('/add-expense-page', methods=['POST'])
def add_expense_html():
    name = request.form.get('name')
    category = request.form.get('category')
    amount = request.form.get('amount')
    date = request.form.get('date')

    tracker.add_expense(name, category, amount, date)

    print("DEBUG:", name, category, amount, date)
    with open("expenses.txt", "a", encoding="utf-8") as f:
        f.write(f"{name},{category},{amount},{date}\n")

    categories = tracker.get_categories()
    recent_expenses = get_recent_expenses()

    # Clean message for frontend
    result_message = "Expense added successfully!"

    return render_template(
        "add_expense.html",
        categories=categories,
        result=result_message,
        recent_expenses=recent_expenses
    )

@app.route('/delete-expense/<int:index>', methods=['POST'])
def delete_expense(index):
    try:
        with open("expenses.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Remove the selected expense
        lines.pop(index)

        with open("expenses.txt", "w", encoding="utf-8") as f:
            f.writelines(lines)

    except (FileNotFoundError, IndexError):
        pass  # Ignore if nothing to delete

    return redirect("/expense-form")


# --------Budget Tracker---------

# @app.route('/set-budget', methods=['POST'])
# def set_budget():
#     try:
#         data = request.get_json()
#         amount = float(data.get("amount", 0))
#         tracker.set_budget(amount)
#         return jsonify({"message": "Budget updated successfully!"})
#     except:
#         return jsonify({"error": "Invalid amount"}), 400
    

# # Backend budget summary
# @app.route('/budget-status', methods=['GET'])
# def budget_status():
#     budget = tracker.get_budget()
#     summary = tracker.get_summary(budget)
#     return jsonify(summary)

# # Frontend budget summary
# @app.route('/budget-summary-page')
# def budget_summary_html():
#     budget = tracker.get_budget()
#     summary = tracker.get_summary(budget)
#     return render_template("budget_summary.html", summary=summary)

# # ===============================
# # PIE CHART DATA API
# # ===============================

# @app.route('/expense-chart-data', methods=['GET'])
# def expense_chart_data():
#     expenses = tracker.get_all_expenses()

#     category_totals = {}
#     for e in expenses:
#         category = e["category"]
#         category_totals[category] = category_totals.get(category, 0) + float(e["amount"])

#     labels = list(category_totals.keys())
#     values = list(category_totals.values())

#     return jsonify({"labels": labels, "values": values})

# ===============================
# BUDGET — SET & VIEW
# ===============================

# Save budget amount
@app.route('/set-budget', methods=['POST'])
def set_budget():
    try:
        data = request.get_json()
        amount = float(data.get("amount", 0))
        tracker.set_budget(amount)
        return jsonify({"message": "Budget updated successfully!"})
    except:
        return jsonify({"error": "Invalid amount"}), 400


# API — Get budget + summary (JSON)
@app.route('/budget-status', methods=['GET'])
def budget_status():
    budget = tracker.get_budget()
    summary = tracker.get_summary(budget)
    return jsonify(summary)


# HTML page — Budget summary page (loads chart + summary)
@app.route('/budget-summary-page')
def budget_summary_html():
    budget = tracker.get_budget()
    summary = tracker.get_summary(budget)
    return render_template("budget_summary.html", summary=summary)


# ===============================
# PIE CHART DATA API
# ===============================

@app.route('/expense-chart-data', methods=['GET'])
def expense_chart_data():
    expenses = tracker.get_all_expenses()

    category_totals = {}
    for e in expenses:
        category = e["category"]
        category_totals[category] = category_totals.get(category, 0) + e["amount"]

    return jsonify(category_totals)

# ==========================
# LOAN RECOMMENDER
# ==========================

@app.route('/loan-recommender-page', methods=['GET'])
def loan_recommender_page():
    return render_template("loan_recommendation.html")   # Loads HTML page


@app.route('/loan-recommender', methods=['POST'])
def loan_recommend_route():
    try:
        data = request.get_json()

        land_type = data.get('LandType')
        land_size = float(data.get('LandSize'))
        location = data.get('Location')
        crop = data.get('CropType')
        income = int(data.get('Income'))

        result = get_loan_recommendation(land_type, land_size, location, crop, income)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

if __name__ == '__main__':
    print("✅ Starting Flask server...")
    app.run(debug=True)
