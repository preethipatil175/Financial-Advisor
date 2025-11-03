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

def get_clean_input(prompt_en, prompt_kn, valid_options, corrections={}):
    while True:
        value = input(f"{prompt_en} / {prompt_kn}: ").strip().lower()
        value = corrections.get(value, value)
        if value in valid_options:
            return value
        print("Invalid input. Try again. / ತಪ್ಪಾದ ಇನ್‌ಪುಟ್. ದಯವಿಟ್ಟು ಪುನಃ ಪ್ರಯತ್ನಿಸಿ.")

def main():
    print(" Farmer Financial Advisor (English + Kannada Support)")

    # Input corrections
    term_corrections = {"midium": "medium", "mediam": "medium"}
    risk_corrections = {"modrate": "moderate", "agrassive": "aggressive"}

    # Inputs
    risk_profile = get_clean_input("Enter risk profile (conservative/moderate/aggressive)",
                                   "ಹೂಡಿಕೆದಾರರ ಅಪಾಯ ಪ್ರೊಫೈಲ್ ನಮೂದಿಸಿ (conservative/moderate/aggressive)",
                                   risk_term_mapping, risk_corrections)

    investment_term = get_clean_input("Enter term (short/medium/long)",
                                      "ಅವಧಿಯನ್ನು ನಮೂದಿಸಿ (short/medium/long)",
                                      investment_term_mapping, term_corrections)

    try:
        initial_amount = float(input("Enter initial capital (INR) / ಆರಂಭಿಕ ಮೊತ್ತವನ್ನು ನಮೂದಿಸಿ (ರೂ): "))
        monthly_saving = float(input("Enter monthly savings (INR) / ಮಾಸಿಕ ಉಳಿತಾಯವನ್ನು ನಮೂದಿಸಿ (ರೂ): "))
    except ValueError:
        print(" Please enter valid numbers. / ದಯವಿಟ್ಟು ಸರಿಯಾದ ಸಂಖ್ಯೆಗಳನ್ನೇ ನಮೂದಿಸಿ.")
        return

    time_years = {"short": 5, "medium": 10, "long": 20}[investment_term]
    total_contribution = monthly_saving * 12 * time_years
    total_investment = initial_amount + total_contribution

    # Gemini Prompt
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

Example:
{{
  "portfolio": [
    {{
      "recommendation": "Buy solar water pump",
      "recommendation_kn": "ಸೌರಜಲ ಪಂಪ್ ಖರೀದಿಸಿ",
      "percentage": 20
    }},
    ...
  ],
  "rationale": "This is suitable for short-term needs.",
  "rationale_kn": "ಇದು ಕಿರುಕಾಲದ ಅಗತ್ಯಗಳಿಗೆ ಸೂಕ್ತವಾಗಿದೆ.",
  "expected_annual_return": 6.8,
  "risk_level": "medium"
}}

Make sure JSON is valid, Kannada is accurate, and percentages total 100.
"""

    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt)
        llm_text = response.text.strip()

        # Extract JSON from Gemini output
        json_start = llm_text.find('{')
        json_end = llm_text.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            raise ValueError("Invalid JSON format in Gemini output")

        json_str = llm_text[json_start:json_end]
        recommendation = json.loads(json_str)

        # Normalize percentages
        total_percentage = sum(item["percentage"] for item in recommendation["portfolio"])
        if not 99.0 <= total_percentage <= 101.0:
            recommendation["portfolio"] = normalize_percentages(recommendation["portfolio"])

        # Output
        print("\n Recommended Portfolio:")
        for item in recommendation["portfolio"]:
            print(f"- {item['recommendation']} ({item['recommendation_kn']}) — {item['percentage']}%")

        print(f"\n Expected Annual Return: {recommendation['expected_annual_return']}%")
        print(f" Risk Level: {recommendation['risk_level']}")
        print(f"\n Rationale (English): {recommendation['rationale']}")
        print(f" ವಿವರಣೆ (ಕನ್ನಡ): {recommendation['rationale_kn']}")

    except Exception as e:
        print(f" Error: {str(e)}")

if __name__ == "__main__":
    main()
