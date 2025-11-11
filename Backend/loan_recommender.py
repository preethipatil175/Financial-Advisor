#!/usr/bin/env python
# coding: utf-8

# In[24]:


# import pandas as pd
# import numpy as np
# import random

# crop_data = {
#     "Rice": {
#         "LoanName": ["Kisan Credit Card", "Crop Loan", "Irrigation Loan"],
#         "Districts": ["Mandya", "Raichur", "Mysuru", "Shivamogga"],
#         "LandTypes": ["Irrigated", "Wetland"],
#         "IncomeRange": (30000, 40000),
#         "LandSizeRange": (1.0, 4.0)
#     },
#     "Wheat": {
#         "LoanName": ["Crop Loan", "PM Kisan Loan"],
#         "Districts": ["Vijayapura", "Bagalkot", "Kalaburagi"],
#         "LandTypes": ["Irrigated", "Dryland"],
#         "IncomeRange": (25000, 35000),
#         "LandSizeRange": (1.5, 5.0)
#     },
#     "Sugarcane": {
#         "LoanName": ["Agricultural Term Loan", "Irrigation Loan", "Farm Mechanization Loan"],
#         "Districts": ["Belagavi", "Mandya", "Mysuru", "Bagalkot"],
#         "LandTypes": ["Irrigated", "Black cotton soil land"],
#         "IncomeRange": (45000, 60000),
#         "LandSizeRange": (2.0, 6.0)
#     },
#     "Millets": {
#         "LoanName": ["Organic Farming Loan", "PM Kisan Loan", "Soil Health Card Loan"],
#         "Districts": ["Chitradurga", "Ballari", "Tumakuru", "Koppal"],
#         "LandTypes": ["Rainfed", "Dryland"],
#         "IncomeRange": (15000, 22000),
#         "LandSizeRange": (2.0, 6.0)
#     },
#     "Pulses": {
#         "LoanName": ["PM Kisan Loan", "Organic Farming Loan", "NABARD Loan"],
#         "Districts": ["Bidar", "Dharwad", "Gadag", "Raichur"],
#         "LandTypes": ["Rainfed", "Dryland"],
#         "IncomeRange": (18000, 25000),
#         "LandSizeRange": (1.0, 4.0)
#     },
#     "Cotton": {
#         "LoanName": ["Crop Loan", "Kisan Credit Card", "Pest Management Loan"],
#         "Districts": ["Haveri", "Gadag", "Dharwad", "Ballari"],
#         "LandTypes": ["Black cotton soil land", "Dryland"],
#         "IncomeRange": (30000, 45000),
#         "LandSizeRange": (2.0, 5.0)
#     },
#     "Coffee": {
#         "LoanName": ["Horticulture Loan", "NABARD Loan", "Plantation Development Loan"],
#         "Districts": ["Kodagu", "Chikkamagaluru", "Hassan"],
#         "LandTypes": ["Wetland", "Black cotton soil land"],
#         "IncomeRange": (60000, 90000),
#         "LandSizeRange": (0.5, 2.0)
#     },
#     "Tea": {
#         "LoanName": ["Plantation Development Loan", "NABARD Refinance Scheme"],
#         "Districts": ["Chikkamagaluru"],
#         "LandTypes": ["Wetland", "Hill slope"],
#         "IncomeRange": (70000, 100000),
#         "LandSizeRange": (1.0, 2.5)
#     },
#     "Mango": {
#         "LoanName": ["Horticulture Loan", "Organic Farming Loan"],
#         "Districts": ["Ramanagara", "Kolar", "Chikkaballapur"],
#         "LandTypes": ["Dryland", "Black cotton soil land"],
#         "IncomeRange": (35000, 60000),
#         "LandSizeRange": (1.0, 4.0)
#     },
#     "Banana": {
#         "LoanName": ["Horticulture Loan", "Irrigation Loan"],
#         "Districts": ["Mandya", "Hassan", "Mysuru"],
#         "LandTypes": ["Irrigated", "Wetland"],
#         "IncomeRange": (40000, 55000),
#         "LandSizeRange": (1.5, 3.5)
#     },
#     "Groundnut": {
#         "LoanName": ["Crop Loan", "Organic Farming Loan"],
#         "Districts": ["Tumakuru", "Chikkaballapur", "Bengaluru Rural"],
#         "LandTypes": ["Dryland", "Black cotton soil land"],
#         "IncomeRange": (20000, 35000),
#         "LandSizeRange": (2.0, 5.0)
#     },
#     "Silk": {
#         "LoanName": ["Sericulture Loan", "NABARD Loan", "Agricultural Term Loan"],
#         "Districts": ["Ramanagara", "Kolar", "Chikkaballapur"],
#         "LandTypes": ["Irrigated", "Dryland"],
#         "IncomeRange": (50000, 75000),
#         "LandSizeRange": (1.0, 3.0)
#     },
#     "Fish Farming": {
#         "LoanName": ["Fisheries Loan", "NABARD Infrastructure Loan"],
#         "Districts": ["Udupi", "Dakshina Kannada", "Uttara Kannada"],
#         "LandTypes": ["Wetland"],
#         "IncomeRange": (60000, 100000),
#         "LandSizeRange": (0.5, 2.5)
#     },
#     "Beekeeping": {
#         "LoanName": ["Apiculture Loan", "Agri Clinic Loan"],
#         "Districts": ["Kodagu", "Shivamogga", "Chamarajanagar"],
#         "LandTypes": ["Dryland", "Forest edge"],
#         "IncomeRange": (50000, 70000),
#         "LandSizeRange": (0.5, 2.0)
#     },
#     "Organic Vegetables": {
#         "LoanName": ["Organic Farming Loan", "Horticulture Loan"],
#         "Districts": ["Mysuru", "Dharwad", "Tumakuru"],
#         "LandTypes": ["Irrigated", "Dryland"],
#         "IncomeRange": (35000, 50000),
#         "LandSizeRange": (1.0, 3.0)
#     },
#     "Floriculture": {
#         "LoanName": ["Floriculture Loan", "NABARD Loan"],
#         "Districts": ["Bengaluru Urban", "Doddaballapura", "Tumakuru"],
#         "LandTypes": ["Irrigated", "Polyhouse"],
#         "IncomeRange": (50000, 80000),
#         "LandSizeRange": (0.5, 2.0)
#     },
#     "Coconut": {
#         "LoanName": ["Plantation Loan", "Agri Infrastructure Loan"],
#         "Districts": ["Dakshina Kannada", "Udupi", "Tumakuru"],
#         "LandTypes": ["Irrigated", "Coastal loamy"],
#         "IncomeRange": (40000, 60000),
#         "LandSizeRange": (1.0, 4.0)
#     },
#     "Maize": {
#         "LoanName": ["Crop Loan", "Farm Mechanization Loan"],
#         "Districts": ["Davanagere", "Gadag", "Chikkaballapur"],
#         "LandTypes": ["Dryland", "Rainfed"],
#         "IncomeRange": (20000, 35000),
#         "LandSizeRange": (2.0, 5.0)
#     },

# }

# # Function to generate synthetic dataset
# def generate_dataset(num_samples=10000):
#     records = []
#     for _ in range(num_samples):
#         crop = random.choice(list(crop_data.keys()))
#         entry = crop_data[crop]
#         loan = random.choice(entry["LoanName"])
#         district = random.choice(entry["Districts"])
#         land_type = random.choice(entry["LandTypes"])
#         income = random.randint(*entry["IncomeRange"])
#         land_size = round(random.uniform(*entry["LandSizeRange"]), 2)

#         records.append([crop, loan, district, land_type, land_size, income])

#     df = pd.DataFrame(records, columns=["CropType", "LoanName", "Location", "LandType", "LandSize", "Income"])
#     return df

# # Generate the dataset
# df = generate_dataset(10000)

# # Display a sample
# print(df.head())

# # Save to CSV (optional)
# df.to_csv("project_dataset.csv", index=False)
# print("project dataset is savved successfully:")


# # In[25]:


# print(df.isnull().sum())


# # In[26]:


# print(df.shape)


# # In[27]:


# import seaborn as sns
# import matplotlib.pyplot as plt

# plt.figure(figsize=(14, 6))
# sns.countplot(x='LoanName', data=df)
# plt.title("Distribution of Loan")
# plt.xticks(rotation=45)
# plt.show()


# # In[28]:


# # CropType distribution
# plt.figure(figsize=(14, 6))
# sns.countplot(x='CropType', data=df)
# plt.title("Distribution of Crops")
# plt.xticks(rotation=45)
# plt.show()

# # LandType distribution
# plt.figure(figsize=(10, 5))
# sns.countplot(x='LandType', data=df)
# plt.title("Distribution of Land Types")
# plt.xticks(rotation=45)
# plt.show()


# # In[29]:


# # pip install imbalanced-learn


# # In[30]:


# from imblearn.over_sampling import RandomOverSampler
# import pandas as pd

# # Step 1: Load your dataset
# df = pd.read_csv("project_dataset.csv")  # Replace with your dataset file

# # Step 2: Separate features and target
# X = df.drop('LoanName', axis=1)  # All features
# y = df['LoanName']               # Target column (class to balance)

# # Step 3: Apply RandomOverSampler
# ros = RandomOverSampler(random_state=42)
# X_resampled, y_resampled = ros.fit_resample(X, y)

# # Step 4: Combine back to a DataFrame
# df_balanced = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled, name='LoanName')], axis=1)

# # Step 5: Save or inspect
# df_balanced.to_csv("balanced_dataset.csv", index=False)
# print(df_balanced['LoanName'].value_counts())


# # In[31]:


# import seaborn as sns
# import matplotlib.pyplot as plt

# sns.countplot(data=df_balanced, x='LoanName')
# plt.xticks(rotation=90)
# plt.title("Balanced Loan Distribution")
# plt.show()


# # In[32]:


# # CropType distribution
# plt.figure(figsize=(14, 6))
# sns.countplot(x='Location', data=df)
# plt.title("Distribution of Districts")
# plt.xticks(rotation=45)
# plt.show()


# # In[33]:


# import pandas as pd
# from sklearn.utils import resample

# # Load your dataset
# df = pd.read_csv("balanced_dataset.csv")  # Replace with your file path

# # Find minimum count per district
# min_count = df['Location'].value_counts().min()

# # Undersample each district to min_count
# balanced_df = (
#     df.groupby('Location')
#     .apply(lambda x: x.sample(n=min_count, random_state=42))
#     .reset_index(drop=True)
# )

# # Check distribution
# print(balanced_df['Location'].value_counts())

# # Optional: Save it
# balanced_df.to_csv("district_balanced_dataset.csv", index=False)


# # In[34]:


# import seaborn as sns
# import matplotlib.pyplot as plt

# sns.countplot(data=balanced_df, x='Location')
# plt.xticks(rotation=90)
# plt.title("Balanced District Distribution")
# plt.tight_layout()
# plt.show()


# # In[35]:


# import pandas as pd

# # Assuming your DataFrame is named df and column is 'LandType'
# min_count = df['LandType'].value_counts().min()

# balanced_land_df = (
#     df.groupby('LandType')
#     .apply(lambda x: x.sample(n=min_count, random_state=42))
#     .reset_index(drop=True)
# )

# # Plot again to verify
# import seaborn as sns
# import matplotlib.pyplot as plt

# plt.figure(figsize=(10, 6))
# sns.countplot(data=balanced_land_df, x='LandType')
# plt.title("Balanced Distribution of Land Types (After Undersampling)")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
# balanced_land_df.to_csv("landtypes_balanced_dataset.csv", index=False)



# # In[38]:


# data = df


# # In[39]:


# from imblearn.over_sampling import RandomOverSampler
# from imblearn.under_sampling import RandomUnderSampler
# import pandas as pd

# # Separate features and target
# X = df.drop(columns=['CropType'])
# y = df['CropType']

# # Step 1: Undersample majority classes
# undersample = RandomUnderSampler(sampling_strategy='not majority', random_state=42)
# X_under, y_under = undersample.fit_resample(X, y)

# # Step 2: Oversample minority classes
# oversample = RandomOverSampler(sampling_strategy='auto', random_state=42)
# X_balanced, y_balanced = oversample.fit_resample(X_under, y_under)

# # Combine back to a DataFrame
# balanced_df = pd.concat([X_balanced, y_balanced], axis=1)


# # In[40]:


# import seaborn as sns
# import matplotlib.pyplot as plt

# plt.figure(figsize=(12, 6))
# sns.countplot(data=balanced_df, x='CropType')
# plt.title("Balanced Crop Types Distribution")
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()


# # In[41]:


# import pandas as pd
# from imblearn.under_sampling import RandomUnderSampler
# from imblearn.over_sampling import RandomOverSampler
# import seaborn as sns
# import matplotlib.pyplot as plt

# # ---------- STEP 1: Load your dataset ----------
# # Replace with your actual dataset
# # df = pd.read_csv("your_dataset.csv")

# # Example: If you already have it loaded in memory
# # Ensure the dataset name is correct
# # If unsure, run: %whos

# # ---------- STEP 2: Select Features to Balance ----------
# features_to_balance = ['CropType', 'LandType', 'LoanName', 'Location']

# # ---------- STEP 3: Loop through each feature and balance it ----------
# balanced_df = df.copy()

# for feature in features_to_balance:
#     print(f"Balancing feature: {feature}")
    
#     # Step 3.1: Prepare data for sampling
#     X = balanced_df.drop(columns=[feature])
#     y = balanced_df[feature]
    
#     # Step 3.2: Undersample the majority class first
#     under = RandomUnderSampler(sampling_strategy='majority', random_state=42)
#     X_under, y_under = under.fit_resample(X, y)
    
#     # Step 3.3: Oversample the minority classes to match
#     over = RandomOverSampler(sampling_strategy='not majority', random_state=42)
#     X_balanced, y_balanced = over.fit_resample(X_under, y_under)
    
#     # Step 3.4: Merge back the target column
#     X_balanced[feature] = y_balanced
#     balanced_df = X_balanced

#     # Step 3.5: Visualize distribution
#     plt.figure(figsize=(8, 4))
#     sns.countplot(data=balanced_df, x=feature)
#     plt.title(f"Balanced Distribution of {feature}")
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()

# # ---------- STEP 4: Final Check ----------
# print("Final dataset shape:", balanced_df.shape)
# print("Null values:\n", balanced_df.isnull().sum())

# # Optional: Save the balanced dataset
# balanced_df.to_csv("landtypes_balanced_dataset.csv", index=False)


# # In[42]:


# import pandas as pd

# # Load the dataset from CSV
# landtypes_balanced_dataset = pd.read_csv("landtypes_balanced_dataset.csv")


# # In[43]:


# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from xgboost import XGBClassifier
# from sklearn.metrics import classification_report

# df = pd.read_csv("landtypes_balanced_dataset.csv")
# df.head()


# # Step 2: Encode categorical columns
# le_land = LabelEncoder()
# le_location = LabelEncoder()
# le_crop = LabelEncoder()
# le_loan = LabelEncoder()  # target

# df['LandType'] = le_land.fit_transform(df['LandType'])
# df['Location'] = le_location.fit_transform(df['Location'])
# df['CropType'] = le_crop.fit_transform(df['CropType'])
# df['LoanName'] = le_loan.fit_transform(df['LoanName'])  # target

# # Step 3: Select only the required 5 features and target
# X = df[['LandType', 'LandSize', 'Location', 'CropType', 'Income']]
# y = df['LoanName']

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# model = XGBClassifier(eval_metric='mlogloss', random_state=42)
# model.fit(X_train, y_train)

# y_pred = model.predict(X_test)
# print(classification_report(y_test,y_pred))


# # In[45]:


# # ✅ FUNCTION: Safe encode for unseen categories
# def safe_label_encode(le: LabelEncoder, value: str):
#     if value not in le.classes_:
#         le.classes_ = np.append(le.classes_, value)
#     return le.transform([value])[0]


# # ✅ User Input and Prediction
# print("\n💬 Enter Farmer Details for Loan Recommendation:")

# user_land_type = input("Land Type (Irrigated, Rainfed, Wetland, Dryland, Black cotton soil, Hill slope, Coastal loamy): ").strip()
# user_land_size = float(input("Land Size (in acres): ").strip())
# user_location = input("Location (Tumkuru, Mandya, Belgaum, Dharwad, Hassan, Raichur, Mysuru, Shivamogga, Vijayapura, Bagalkot, Kalaburagi, Belagavi, Chitradurga, Ballari, Koppal, Bidar, Chikkamagaluru, Gadag, Haveri, Kodagu, Ramanagara, Kolar, Chikkaballapur, Udupi, Uttara Kannada): ").strip()
# user_crop_type = input("Crop Type (Rice, Wheat, Cotton, Sugarcane, Pulses, Millets, Coffee, Tea, Mango, Banana, Groundnut, Silk, Fish Farming, Beekeeping, Organic Vegetables, Floriculture, Coconut, Maize): ").strip()
# user_income = int(input("Income : ").strip())

# try:
#     # Encode inputs safely
#     encoded_land_type = safe_label_encode(le_land, user_land_type)
#     encoded_location = safe_label_encode(le_location, user_location)
#     encoded_crop_type = safe_label_encode(le_crop, user_crop_type)

#     input_data = [[
#         encoded_land_type,
#         user_land_size,
#         encoded_location,
#         encoded_crop_type,
#         user_income
#     ]]

#     # Predict top 3 recommended loans
#     probs = model.predict_proba(input_data)[0]
#     top_indices = probs.argsort()[::-1][:3]
#     top_loans = le_loan.inverse_transform(top_indices)

#     # Output
#     print("\n✅ Best Recommended Loan:", top_loans[0])
#     if len(top_loans) > 1:
#         print("💡 Other Suitable Loan Options:", ", ".join(top_loans[1:]))

# except Exception as e:
#     print("❌ Something went wrong:", e)


# # In[47]:


# df.shape


# # In[ ]:




import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import joblib


# Load trained model
# model = joblib.load("loan_model.pkl")


# # Load encoders
# le_land = joblib.load("le_land.pkl")
# le_location = joblib.load("le_location.pkl")
# le_crop = joblib.load("le_crop.pkl")
# le_loan = joblib.load("le_loan.pkl")  # target encoder


# Function to safely encode unseen labels
def safe_label_encode(le: LabelEncoder, value: str):
    if value not in le.classes_:
        le.classes_ = np.append(le.classes_, value)
    return le.transform([value])[0]


# ✅ FUNCTION to be used in Flask
def get_loan_recommendation(land_type, land_size, location, crop, income):

    try:
        enc_land = safe_label_encode(le_land, land_type)
        enc_location = safe_label_encode(le_location, location)
        enc_crop = safe_label_encode(le_crop, crop)

        input_data = [[enc_land, land_size, enc_location, enc_crop, income]]

        # Predict top 3
        probs = model.predict_proba(input_data)[0]
        top_idx = probs.argsort()[::-1][:3]
        top_loans = le_loan.inverse_transform(top_idx)

        return {
            "best_loan": top_loans[0],
            "other_options": list(top_loans[1:])
        }

    except Exception as e:
        return {"error": str(e)}
