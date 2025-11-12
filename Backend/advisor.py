import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Mappings
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

def normalize_percentages(portfolio):
    total = sum(item["percentage"] for item in portfolio)
    return [
        {
            "recommendation": item["recommendation"],
            "recommendation_kn": item["recommendation_kn"],
            "percentage": round((item["percentage"] / total) * 100, 1)
        }
        for item in portfolio
    ]

def get_financial_advice(risk_profile, investment_term, initial_amount, monthly_saving):
    if risk_profile not in risk_term_mapping:
        return {"error": "Invalid risk profile"}

    if investment_term not in investment_term_mapping:
        return {"error": "Invalid investment term"}

    try:
        initial_amount = float(initial_amount)
        monthly_saving = float(monthly_saving)
    except ValueError:
        return {"error": "Invalid numeric values"}

    time_years = {"short": 5, "medium": 10, "long": 20}[investment_term]
    total_contribution = monthly_saving * 12 * time_years
    total_investment = initial_amount + total_contribution

    prompt = f"""
You are a rural financial advisor for Indian farmers with 15+ years of experience.

Suggest a financial portfolio based on:
- Risk Profile: {risk_profile} ({risk_term_mapping[risk_profile]})
- Term: {investment_term} ({investment_term_mapping[investment_term]})
- Initial Capital: ₹{initial_amount:,.2f}
- Monthly Saving: ₹{monthly_saving:,.2f}
- Total estimated investment: ₹{total_investment:,.2f}

Return JSON with:
1. A portfolio of 5–8 financial suggestions.
2. Each suggestion must include:
   - "recommendation": English
   - "recommendation_kn": Kannada translation
   - "percentage": allocation (%)
3. Two rationale fields:
   - "rationale": English explanation
   - "rationale_kn": Kannada explanation
4. "expected_annual_return" (%)
5. "risk_level" (low, medium, high)

Make sure JSON is valid, Kannada is accurate, and percentages total 100.
"""

    try:
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        response = model.generate_content(prompt)
        llm_text = response.text.strip()

        json_start = llm_text.find('{')
        json_end = llm_text.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            return {"error": "Invalid JSON format in Gemini output"}

        json_str = llm_text[json_start:json_end]
        recommendation = json.loads(json_str)

        total_percentage = sum(item["percentage"] for item in recommendation["portfolio"])
        if not 99.0 <= total_percentage <= 101.0:
            recommendation["portfolio"] = normalize_percentages(recommendation["portfolio"])

        return recommendation

    except Exception as e:
        return {"error": str(e)}
