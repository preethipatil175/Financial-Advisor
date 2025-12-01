🌾 Farmers Wallet
AI-Powered Financial Management Platform for Farmers

A comprehensive Flask-based web application providing farmers with intelligent financial advice, crop price forecasting, expense tracking, budget management, and personalized loan recommendations.

✨ Key Features
💡 Financial Advice & Crop Planning
AI-powered personalized investment strategies using Google Gemini
Risk profile-based recommendations (Conservative, Balanced, Aggressive)
Investment term planning (Short, Medium, Long-term)
Multilingual support (English, Hindi, Kannada, Tamil, Telugu, Malayalam)
📊 Crop Price Forecasting
Machine Learning-based price predictions
Supported crops: Wheat, Cotton, Sugarcane, Jowar, Bajra
Historical trend analysis with rainfall data
Price range forecasting (min, max, average)
💰 Expense Tracking & Budgeting
Track daily farming expenses across 16 categories
Set and monitor monthly budgets
Real-time budget utilization tracking
Visual analytics with pie charts and trend graphs
Export data to CSV
🏦 Loan Recommendations
XGBoost-based intelligent loan matching
Analyzes: crop type, land type, location (30 Karnataka districts), land size, income
Top 3 personalized loan recommendations
Government scheme integration
🛠 Technology Stack
Component	Technology
Backend	Flask 3.1, Python 3.9+
Frontend	HTML5, CSS3, JavaScript (Vanilla)
AI/ML	Google Generative AI (Gemini 2.0), XGBoost, scikit-learn
Data Processing	Pandas, NumPy
Visualization	Chart.js
Icons	Font Awesome 6.5
📁 Project Structure
Farmers Wallet Final/
├── code_1/                          # Main application directory
│   ├── app_new.py                   # Flask application entry point
│   ├── crop_price.py                # Crop price prediction engine
│   ├── exp_budget.py                # Expense tracking & budget management
│   ├── loan_recommender.py          # Loan recommendation system
│   ├── requirements-clean.txt       # Python dependencies
│   │
│   ├── static/                      # Static assets
│   │   ├── css/
│   │   │   └── main.css            # Main stylesheet
│   │   └── js/
│   │       └── main.js             # Client-side JavaScript
│   │
│   ├── templates/                   # HTML templates
│   │   ├── home.html               # Landing page
│   │   ├── financial_combined.html # Financial advice interface
│   │   ├── crop_prediction.html    # Price forecasting interface
│   │   ├── expense_form.html       # Expense entry form
│   │   ├── budget_summary.html     # Budget dashboard
│   │   └── loan_recommendations.html # Loan suggestions interface
│   │
│   ├── jupyter_files/               # ML model training notebooks
│   │   ├── *.ipynb                 # Jupyter notebooks
│   │   ├── *.csv                   # Training datasets
│   │   └── *_preprocessor.pkl      # Feature preprocessors
│   │
│   ├── ML Models (*.pkl files)
│   │   ├── jmodel.pkl              # Jowar price model
│   │   ├── wmodel.pkl              # Wheat price model
│   │   ├── cmodel.pkl              # Cotton price model
│   │   ├── smodel.pkl              # Sugarcane price model
│   │   └── bmodel.pkl              # Bajra price model
│   │
│   └── Data Files
│       ├── farmer_expenses.csv      # Expense records
│       ├── farmer_categories.json   # Expense categories
│       └── farmer_budget.txt        # Budget amount
│
├── farmer_Loan_recommender-main/    # Loan ML system
│   ├── loan_recomm.ipynb           # Model training notebook
│   ├── loan_model.pkl              # Trained XGBoost model
│   ├── label_encoders.pkl          # Feature encoders
│   └── project_dataset.xls         # Training dataset
│
├── .env                             # Environment variables (API keys)
├── .venv/                           # Python virtual environment
├── README.md                        # This file
└── SETUP.md                         # Detailed setup instructions
🚀 Quick Start
Prerequisites
Python 3.9 or higher
pip package manager
Google API Key - Get one here
Installation Steps
Navigate to project directory:

cd "/Users/aadhavanap/Desktop/Farmer's Wallet Final"
Create and activate virtual environment:

python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
Install dependencies:

pip install -r code_1/requirements-clean.txt
Configure environment variables:

Create/edit .env file in project root:

GOOGLE_API_KEY=your_actual_google_api_key_here
Run the application:

python3 code_1/app_new.py
Access the application:

Open your browser and navigate to:

http://localhost:5001
📝 API Endpoints
Core Routes
Method	Endpoint	Description
GET	/	Home page
GET/POST	/financial-advice	AI financial advisor
GET/POST	/price-form	Crop price forecasting
GET	/expense-form	Expense tracking form
GET	/budget-summary-page	Budget dashboard
GET	/loan-recommendations	Loan recommendations
Expense Management API
Method	Endpoint	Description
POST	/add-expense	Add new expense
POST	/delete-expense	Delete expense by index
POST	/clear-all-expenses	Clear all expenses
POST	/set-budget	Set monthly budget
GET	/get-summary	Get expense summary & charts
GET	/get-expenses	Get all expenses
GET	/get-categories	Get expense categories
Prediction APIs
Method	Endpoint	Description
POST	/predict-price	Get crop price prediction (JSON)
POST	/get-loan-recommendations	Get loan suggestions (JSON)
🎨 Features in Detail
Expense Categories (16 Total)
Seeds & Planting
Equipment & Machinery
Irrigation & Water
Fertilizers
Pesticides & Chemicals
Labor Costs
Transportation
Market & Selling
Food & Personal
Household
Fuel & Energy
Veterinary & Livestock
Maintenance & Repairs
Loan & Interest
Communication
Miscellaneous
Supported Languages
🇬🇧 English
🇮🇳 Hindi (हिंदी)
🇮🇳 Kannada (ಕನ್ನಡ)
🇮🇳 Tamil (தமிழ்)
🇮🇳 Telugu (తెలుగు)
🇮🇳 Malayalam (മലയാളം)
Karnataka Districts (30)
Bagalkot, Ballari, Belagavi, Bengaluru Rural, Bengaluru Urban, Bidar, Chamarajanagar, Chikkaballapur, Chikkamagaluru, Chitradurga, Dakshina Kannada, Davanagere, Dharwad, Gadag, Hassan, Haveri, Kalaburagi, Kodagu, Kolar, Koppal, Mandya, Mysuru, Raichur, Ramanagara, Shivamogga, Tumakuru, Udupi, Uttara Kannada, Vijayapura, Yadgir

🔧 Configuration
Flask Settings
Located in code_1/app_new.py:

app.run(host='0.0.0.0', port=5001, debug=True)
Change Port (if 5001 is in use):
app.run(host='0.0.0.0', port=5002, debug=True)
🐛 Troubleshooting
Port Already in Use
# Find process using port 5001
lsof -ti:5001

# Kill the process
kill -9 $(lsof -ti:5001)

# Or change port in app_new.py
Missing API Key Error
Ensure .env file exists in project root with valid Google API key.

Module Not Found
# Reinstall dependencies
pip install -r code_1/requirements-clean.txt
Model Files Missing
Verify these files exist in code_1/:

jmodel.pkl, wmodel.pkl, cmodel.pkl, smodel.pkl, bmodel.pkl
preprocessor.pkl
📊 Data Management
Reset Everything
Click the Reset button in Budget Summary to:

Clear all expenses
Reset budget to ₹0
Clear all charts
Export Data
Expense data is automatically saved to:

code_1/farmer_expenses.csv
Backup Data
# Backup expense data
cp code_1/farmer_expenses.csv ~/Desktop/expenses_backup.csv

# Backup budget
cp code_1/farmer_budget.txt ~/Desktop/budget_backup.txt
