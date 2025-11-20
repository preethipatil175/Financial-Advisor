from flask import Flask, request, jsonify, render_template,redirect
from advisor import get_financial_advice
from kannadacrop import predict_crop_price
from exp_budget import FarmerExpenseTracker
from loan_system import get_loan_recommendation
from crop_price import ml_predict_price
import google.generativeai as genai
from dotenv import load_dotenv
from markdown import markdown
import os


app = Flask(__name__)

# Initialize expense tracker
tracker = FarmerExpenseTracker()


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

risk_term_mapping = {
    "conservative": "low risk, focused on safety and essential needs",
    "moderate": "balanced risk, some growth and some stability",
    "aggressive": "high risk, focused on expansion and profit"
}

investment_term_mapping = {
    "short": "less than 5 years",
    "medium": "between 5 and 10 years",
    "long": "more than 10 years"
}

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

def get_financial_advice(risk_profile, investment_term, initial_amount, monthly_saving, language):
    try:
        initial_amount = float(initial_amount)
        monthly_saving = float(monthly_saving)

        # Language instruction
        if language == "kannada":
            lang_instruction = "Generate the entire financial advice in Kannada. Avoid English except for numbers."
        else:
            lang_instruction = "Generate the entire financial advice in English."

        prompt = f"""
You are a rural financial advisor for Indian farmers.

{lang_instruction}

Provide detailed financial advice based on:
- Risk Profile: {risk_profile} ({risk_term_mapping[risk_profile]})
- Term: {investment_term} ({investment_term_mapping[investment_term]})
- Initial Amount: ₹{initial_amount}
- Monthly Saving: ₹{monthly_saving}

Do NOT return JSON.
Return a full explanation, portfolio breakdown, tables, and reasoning in clean Markdown format.
"""

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        return {"raw_output": response.text.strip()}

    except Exception as e:
        return {"error": str(e)}


@app.route("/financial-advice", methods=["GET", "POST"])
def index():
    formatted_output = None
    result = None

    if request.method == "POST":
        risk_profile = request.form.get("risk_profile")
        investment_term = request.form.get("investment_term")
        initial_amount = request.form.get("initial_amount")
        monthly_saving = request.form.get("monthly_saving")
        language = request.form.get("language")  # New

        result = get_financial_advice(
            risk_profile,
            investment_term,
            initial_amount,
            monthly_saving,
            language
        )

        if "raw_output" in result:
            formatted_output = markdown(
                result["raw_output"],
                extensions=["extra", "tables", "sane_lists"]
            )

    return render_template("financial_advisor.html", result=result, formatted_output=formatted_output)


# ======================================================================
# ✅ CROP PRICE PREDICTION
# ======================================================================

# Frontend
@app.route('/price-form')
def price_form():
    return render_template("crop_prediction.html")


@app.route('/predict-price-api',methods=['POST'])
def predict_price_api():
    try:
        data = request.json
        crop = data.get('crop')
        month = int(data.get('month'))
        year = int(data.get('year'))
        rainfall = float(data.get('rainfall'))
        lang = data.get('language', 'en')

        # Kannada → English mapping
        kannada_to_english = {
            "ಜೋಳ": "jowar",
            "ಗೋಧಿ": "wheat",
            "ಕಾಟನ್": "cotton",
            "ಬಜ್ರಾ": "bajara",
            "ಸಕ್ಕರೆ": "sugarcane"
        }
        if crop in kannada_to_english:
            crop = kannada_to_english[crop]

        # ML prediction
        predicted_index, min_price, max_price, avg_price = ml_predict_price(
            crop, month, year, rainfall
        )

        return jsonify({
            "predicted_index": predicted_index,
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

            name, amount,category, date = parts
            expenses.append({
                "name": name,
                "amount": amount,
                "category": category,
                "date": date
            })
        return expenses
    except FileNotFoundError:
        return []

kannada_categories = {
    "Seeds & Planting": "ಬೀಜಗಳು ಮತ್ತು ನೆಡುವಿಕೆ",
    "Equipment & Machinery": "ಉಪಕರಣಗಳು ಮತ್ತು ಯಂತ್ರೋಪಕರಣಗಳು",
    "Irrigation & Water": "ನೀರಾವರಿ ಮತ್ತು ನೀರು",
    "Fertilizers": "ರಸಗೊಬ್ಬರಗಳು",
    "Pesticides & Chemicals": "ಕೀಟನಾಶಕಗಳು ಮತ್ತು ರಾಸಾಯನಿಕಗಳು",
    "Labor Costs": "ಕಾರ್ಮಿಕ ವೆಚ್ಚ",
    "Transportation": "ಸಾರಿಗೆ",
    "Market & Selling": "ಮಾರಾಟ ಮತ್ತು ಮಾರುಕಟ್ಟೆ",
    "Food & Personal": "ಆಹಾರ ಮತ್ತು ವೈಯಕ್ತಿಕ",
    "Household": "ಗೃಹ ಬಳಕೆ",
    "Fuel & Energy": "ಇಂಧನ ಮತ್ತು ಶಕ್ತಿ",
    "Veterinary & Livestock": "ಪಶು ವೈದ್ಯಕೀಯ ಮತ್ತು ಪಶುಸಂಗೋಪನೆ",
    "Maintenance & Repairs": "ರಕ್ಷಣೆ ಮತ್ತು ದುರಸ್ತಿ",
    "Loan & Interest": "ಸಾಲ ಮತ್ತು ಬಡ್ಡಿ",
    "Communication": "ಸಂಪರ್ಕ",
    "Miscellaneous": "ಇತರೆ"
}


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
    lang = request.args.get("lang", "en")

    categories = tracker.get_categories()

    if lang == "kn":
        categories = [kannada_categories.get(c, c) for c in categories]

    recent_expenses = get_recent_expenses()

    return render_template(
        "add_expense.html",
        categories=categories,
        recent_expenses=recent_expenses,
        lang=lang
    )

# def expense_form():
#     categories = tracker.get_categories()
#     recent_expenses = get_recent_expenses()
#     return render_template("add_expense.html", categories=categories,recent_expenses=recent_expenses)

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
@app.route("/budget-summary-page",methods=['GET'])
def budget_summary_page():

    # Read total budget
    try:
        with open("farmer_budget.txt", "r") as f:
            total_budget = int(f.read().strip())
    except:
        total_budget = 0

    # Read expenses from file
    expenses = []
    try:
        with open("expenses.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    name, amount, category, date = parts
                    expenses.append({
                        "name": name,
                        "amount": float(amount),
                        "category": category,
                        "date": date
                    })
    except:
        pass

    # Category totals
    category_sums = {}
    for exp in expenses:
        cat = exp["category"]
        amt = exp["amount"]
        category_sums[cat] = category_sums.get(cat, 0) + amt

    categories = list(category_sums.keys())
    values = list(category_sums.values())

    return render_template(
        "budget_summary.html",
        total_budget=total_budget,
        categories=categories,
        values=values
    )


# ===============================
# PIE CHART DATA API (FIXED)
# ===============================
@app.route('/expense-chart-data')
def expense_chart_data():

    # 1️⃣ Read budget
    try:
        with open("farmer_budget.txt", "r") as f:
            budget = float(f.read().strip())
    except:
        budget = 0

    # 2️⃣ Read expenses correctly
    category_totals = {}

    try:
        with open("expenses.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")

                # correct file structure: name, category, amount, date
                if len(parts) == 4:
                    name, category, amount, date = parts

                    try:
                        amount = float(amount)
                    except:
                        continue

                    category_totals[category] = category_totals.get(category, 0) + amount

    except FileNotFoundError:
        pass

    # 3️⃣ Prepare chart data
    labels = list(category_totals.keys())
    values = list(category_totals.values())

    total_spent = sum(values)
    remaining = max(budget - total_spent, 0)

    percentages = [
        (v / budget * 100) if budget > 0 else 0 for v in values
    ]

    # 4️⃣ Send JSON
    return jsonify({
        "labels": labels,
        "values": values,
        "percentages": percentages,
        "budget": budget,
        "total_spent": total_spent,
        "remaining": remaining
    })



# ==========================
# LOAN RECOMMENDER
# ==========================

@app.route('/loan-recommender', methods=['GET'])
def loan_recommender_page():
    return render_template("loan_recommendation.html")   # Loads HTML page


@app.route('/loan-recommender-page', methods=['POST'])
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
