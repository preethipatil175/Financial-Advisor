# # -------------------------------------------------------------
# # 🚀 Loan Recommendation System - XGBoost (90% Accuracy Target)
# # -------------------------------------------------------------
# import pandas as pd
# import numpy as np
# import pickle
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
# from xgboost import XGBClassifier

# # -------------------------------------------------------------
# # 1️⃣ LOAD DATA
# # -------------------------------------------------------------
# print("📘 Loading dataset...")
# df = pd.read_csv(r"C:\Users\Vijaylaxmi\Downloads\Projects\Financial-Advisor\Backend\loan_recommendation_dataset.csv")   # TODO: replace with your dataset path
# print("Dataset Loaded!")
# print(df.head())

# # -------------------------------------------------------------
# # 2️⃣ LABEL ENCODING FOR CATEGORICAL COLUMNS
# # -------------------------------------------------------------
# le_crop = LabelEncoder()
# le_loan = LabelEncoder()
# le_location = LabelEncoder()
# le_land = LabelEncoder()

# df["CropType"] = le_crop.fit_transform(df["CropType"])
# df["LoanName"] = le_loan.fit_transform(df["LoanName"])
# df["Location"] = le_location.fit_transform(df["Location"])
# df["LandType"] = le_land.fit_transform(df["LandType"])

# # -------------------------------------------------------------
# # 3️⃣ PREPARE FEATURES & TARGET
# # -------------------------------------------------------------
# X = df[["CropType", "Location", "LandType", "LandSize", "Income"]]
# y = df["LoanName"]

# # -------------------------------------------------------------
# # 4️⃣ TRAIN-TEST SPLIT
# # -------------------------------------------------------------
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42, stratify=y
# )

# # -------------------------------------------------------------
# # 5️⃣ XGBOOST MODEL (High Accuracy Settings)
# # -------------------------------------------------------------
# model = XGBClassifier(
#     n_estimators=500,
#     max_depth=10,
#     learning_rate=0.05,
#     subsample=0.9,
#     colsample_bytree=0.8,
#     eval_metric="mlogloss"
# )

# print("\n⏳ Training XGBoost Model...")
# model.fit(X_train, y_train)
# print("✔ Training Completed!")

# # -------------------------------------------------------------
# # 6️⃣ MODEL EVALUATION
# # -------------------------------------------------------------
# y_pred = model.predict(X_test)
# acc = accuracy_score(y_test, y_pred)

# print(f"\n🎯 Accuracy: {acc:.4f}")
# print("\n📊 Classification Report:\n")
# print(classification_report(y_test, y_pred))

# # -------------------------------------------------------------
# # 7️⃣ SAVE MODEL & ENCODERS
# # -------------------------------------------------------------
# import os
# os.makedirs("model", exist_ok=True)

# pickle.dump(model, open("model/xgb_model.pkl", "wb"))
# pickle.dump(le_crop, open("model/le_crop.pkl", "wb"))
# pickle.dump(le_loan, open("model/le_loan.pkl", "wb"))
# pickle.dump(le_location, open("model/le_location.pkl", "wb"))
# pickle.dump(le_land, open("model/le_land.pkl", "wb"))

# print("\n💾 Model & Encoders Saved Successfully!")

# # -------------------------------------------------------------
# # 8️⃣ SAFE LABEL ENCODING FOR USER INPUT
# # -------------------------------------------------------------
# def safe_label_encode(le: LabelEncoder, value: str):
#     """Allows encoding unseen values without crashing."""
#     if value not in le.classes_:
#         le.classes_ = np.append(le.classes_, value)
#     return le.transform([value])[0]

# # -------------------------------------------------------------
# # 9️⃣ USER INPUT — LOAN RECOMMENDATION
# # -------------------------------------------------------------
# print("\n💬 Enter Farmer Details for Loan Recommendation:")

# user_land_type = input("Land Type (Irrigated, Rainfed, Wetland, Dryland, Black cotton soil, Hill slope, Coastal loamy): ").strip()
# user_land_size = float(input("Land Size (in acres): ").strip())
# user_location = input("Location (Tumkuru, Mandya, Belgaum, Dharwad, Hassan, Raichur, Mysuru, Shivamogga, Vijayapura, Bagalkot, Kalaburagi, Belagavi, Chitradurga, Ballari, Koppal, Bidar, Chikkamagaluru, Gadag, Haveri, Kodagu, Ramanagara, Kolar, Chikkaballapur, Udupi, Uttara Kannada): ").strip()
# user_crop_type = input("Crop Type (Rice, Wheat, Cotton, Sugarcane, Pulses, Millets, Coffee, Tea, Mango, Banana, Groundnut, Silk, Fish Farming, Beekeeping, Organic Vegetables, Floriculture, Coconut, Maize): ").strip()
# user_income = int(input("Income : ").strip())

# # Encode safely
# e_crop = safe_label_encode(le_crop, user_crop_type)
# e_loc = safe_label_encode(le_location, user_location)
# e_land = safe_label_encode(le_land, user_land_type)

# input_data = [[e_crop, e_loc, e_land, user_land_size, user_income]]

# # Predict
# probs = model.predict_proba(input_data)[0]
# top_indices = probs.argsort()[::-1][:3]
# top_loans = le_loan.inverse_transform(top_indices)

# # -------------------------------------------------------------
# # 🔟 OUTPUT FINAL RESULTS
# # -------------------------------------------------------------
# print("\n===============================")
# print("🎯 **BEST LOAN RECOMMENDATION**")
# print("===============================")
# print("👉 Recommended Loan:", top_loans[0])

# print("\n⭐ Other Suitable Loans:")
# for loan in top_loans[1:]:
#     print("➡", loan)

# loan_system.py
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
