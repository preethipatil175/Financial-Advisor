import numpy as np
import pickle

# -------------------------------------------------------------
# 1️⃣ LOAD MODEL & ENCODERS (Only once)
# -------------------------------------------------------------
model = pickle.load(open("model/xgb_model.pkl", "rb"))
le_crop = pickle.load(open("model/le_crop.pkl", "rb"))
le_loan = pickle.load(open("model/le_loan.pkl", "rb"))
le_location = pickle.load(open("model/le_location.pkl", "rb"))
le_land = pickle.load(open("model/le_land.pkl", "rb"))


# -------------------------------------------------------------
# 2️⃣ SAFE ENCODING FUNCTION
# -------------------------------------------------------------
def safe_encode(le, value):
    """Encode even unseen labels."""
    if value not in le.classes_:
        le.classes_ = np.append(le.classes_, value)
    return le.transform([value])[0]


# -------------------------------------------------------------
# 3️⃣ MAIN FUNCTION CALLED BY FLASK
# -------------------------------------------------------------
def get_loan_recommendation(land_type, land_size, location, crop, income):

    # Safe encoding
    e_crop = safe_encode(le_crop, crop)
    e_loc = safe_encode(le_location, location)
    e_land = safe_encode(le_land, land_type)

    # Prepare input for model
    input_data = [[e_crop, e_loc, e_land, float(land_size), int(income)]]

    # Predict probabilities
    probs = model.predict_proba(input_data)[0]

    # Top 3 loans
    top_indices = probs.argsort()[::-1][:3]
    top_loans = le_loan.inverse_transform(top_indices)

    # Return JSON-ready dict
    return {
        "best_loan": top_loans[0],
        "other_loans": list(top_loans[1:])
    }
