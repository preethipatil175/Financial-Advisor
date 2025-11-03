import datetime
import csv
import os
import json

class Expense:
    def __init__(self, name, category, amount, date=None):
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date or datetime.date.today().strftime("%Y-%m-%d")

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, Rs.{self.amount}>"

class FarmerExpenseTracker:
    def __init__(self):
        self.expense_file_path = "farmer_expenses.csv"
        self.categories_file_path = "farmer_categories.json"
        self.default_categories = [
            "Seeds & Planting",
            "Equipment & Machinery",
            "Irrigation & Water",
            "Fertilizers",
            "Pesticides & Chemicals",
            "Labor Costs",
            "Transportation",
            "Market & Selling",
            "Food & Personal",
            "Household",
            "Fuel & Energy",
            "Veterinary & Livestock",
            "Maintenance & Repairs",
            "Loan & Interest",
            "Communication",
            "Miscellaneous"
        ]
        self.load_categories()

    def load_categories(self):
        if os.path.exists(self.categories_file_path):
            try:
                with open(self.categories_file_path, 'r') as f:
                    self.categories = json.load(f)
            except:
                self.categories = self.default_categories.copy()
                self.save_categories()
        else:
            self.categories = self.default_categories.copy()
            self.save_categories()

    def save_categories(self):
        with open(self.categories_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.categories, f, indent=2)

    def display_welcome(self):
        print("=" * 60)
        print("FARMER EXPENSE TRACKER")
        print("=" * 60)
        print("Track your agricultural expenses efficiently!")
        print("=" * 60)

    def main_menu(self):
        while True:
            print("\nMAIN MENU")
            print("-" * 30)
            print("1. Add New Expense")
            print("2. View Expense Summary")
            print("3. Manage Categories")
            print("4. Set/Update Budget")
            print("5. Monthly Report")
            print("6. Exit")
            print("-" * 30)

            try:
                choice = input("Enter your choice (1-6): ").strip()

                if choice == "1":
                    self.add_expense_flow()
                elif choice == "2":
                    budget = self.get_current_budget()
                    self.summarize_expenses(budget)
                elif choice == "3":
                    self.manage_categories_menu()
                elif choice == "4":
                    self.set_budget()
                elif choice == "5":
                    self.monthly_report()
                elif choice == "6":
                    print("\nThank you for using Farmer Expense Tracker!")
                    break
                else:
                    print("Invalid choice! Please enter 1-6.")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

    def add_expense_flow(self):
        expense = self.get_user_expense()
        if expense:
            self.save_expense_to_file(expense)
            print(f"Expense '{expense.name}' saved successfully!")

    def get_user_expense(self):
        print("\nADDING NEW EXPENSE")
        print("-" * 30)

        try:
            expense_name = input("Enter expense description: ").strip()
            if not expense_name:
                print("Expense name cannot be empty!")
                return None

            while True:
                try:
                    expense_amount = float(input("Enter amount (Rs.): "))
                    if expense_amount <= 0:
                        print("Amount must be greater than 0!")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number!")

            date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if date_input:
                try:
                    datetime.datetime.strptime(date_input, "%Y-%m-%d")
                    expense_date = date_input
                except ValueError:
                    print("Invalid date format! Using today's date.")
                    expense_date = datetime.date.today().strftime("%Y-%m-%d")
            else:
                expense_date = datetime.date.today().strftime("%Y-%m-%d")

            selected_category = self.select_category()
            if not selected_category:
                return None

            return Expense(
                name=expense_name,
                category=selected_category,
                amount=expense_amount,
                date=expense_date
            )

        except KeyboardInterrupt:
            print("\nOperation cancelled!")
            return None

    def select_category(self):
        while True:
            print("\nSELECT CATEGORY")
            print("-" * 30)

            for i, category in enumerate(self.categories):
                print(f"  {i + 1}. {category}")
            print(f"  {len(self.categories) + 1}. Add New Category")
            print(f"  0. Cancel")

            try:
                choice = int(input(f"\nEnter choice (0-{len(self.categories) + 1}): "))

                if choice == 0:
                    return None
                elif 1 <= choice <= len(self.categories):
                    return self.categories[choice - 1]
                elif choice == len(self.categories) + 1:
                    new_category = self.add_new_category()
                    if new_category:
                        return new_category
                else:
                    print("Invalid choice!")

            except ValueError:
                print("Please enter a valid number!")

    def add_new_category(self):
        print("\nADD NEW CATEGORY")
        print("-" * 25)

        category_name = input("Enter new category name: ").strip()
        if not category_name:
            print("Category name cannot be empty!")
            return None

        self.categories.append(category_name)
        self.save_categories()
        print(f"Category '{category_name}' added successfully!")
        return category_name

    def manage_categories_menu(self):
        while True:
            print("\nMANAGE CATEGORIES")
            print("-" * 30)
            print("1. View All Categories")
            print("2. Add New Category")
            print("3. Remove Category")
            print("4. Reset to Default")
            print("5. Back to Main Menu")

            choice = input("Enter choice (1-5): ").strip()

            if choice == "1":
                self.view_categories()
            elif choice == "2":
                self.add_new_category()
            elif choice == "3":
                self.remove_category()
            elif choice == "4":
                self.reset_categories()
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

    def view_categories(self):
        print("\nALL CATEGORIES")
        print("-" * 30)
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")

    def remove_category(self):
        if len(self.categories) <= 1:
            print("Cannot remove category! At least one category is required.")
            return

        self.view_categories()
        try:
            choice = int(input(f"\nEnter category number to remove (1-{len(self.categories)}): "))
            if 1 <= choice <= len(self.categories):
                removed = self.categories.pop(choice - 1)
                self.save_categories()
                print(f"Category '{removed}' removed successfully!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a valid number!")

    def reset_categories(self):
        confirm = input("This will reset all categories to default. Continue? (y/N): ")
        if confirm.lower() in ['y', 'yes']:
            self.categories = self.default_categories.copy()
            self.save_categories()
            print("Categories reset to default!")

    def save_expense_to_file(self, expense):
        file_exists = os.path.exists(self.expense_file_path)

        with open(self.expense_file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Name', 'Amount', 'Category', 'Date'])
            writer.writerow([expense.name, expense.amount, expense.category, expense.date])

    def load_expenses(self):
        expenses = []
        if not os.path.exists(self.expense_file_path):
            return expenses

        try:
            with open(self.expense_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    expense = Expense(
                        name=row['Name'],
                        amount=float(row['Amount']),
                        category=row['Category'],
                        date=row['Date']
                    )
                    expenses.append(expense)
        except Exception as e:
            print(f"Error loading expenses: {e}")

        return expenses

    def summarize_expenses(self, budget=None):
        import calendar
        expenses = self.load_expenses()

        if not expenses:
            print("\nNo expenses recorded yet!")
            return

        print("\nEXPENSE SUMMARY")
        print("=" * 50)

        amount_by_category = {}
        for expense in expenses:
            if expense.category in amount_by_category:
                amount_by_category[expense.category] += expense.amount
            else:
                amount_by_category[expense.category] = expense.amount

        print("Expenses by Category:")
        print("-" * 30)
        for category, amount in sorted(amount_by_category.items()):
            print(f"  {category}: Rs.{amount:,.2f}")

        total_spent = sum(expense.amount for expense in expenses)
        print(f"\nTotal Spent: Rs.{total_spent:,.2f}")

        if budget and budget > 0:
            remaining_budget = budget - total_spent
            print(f"Budget: Rs.{budget:,.2f}")
            print(f"Remaining: Rs.{remaining_budget:,.2f}")

            if remaining_budget < 0:
                print(f"Over budget by: Rs.{abs(remaining_budget):,.2f}")

            now = datetime.datetime.now()
            days_in_month = calendar.monthrange(now.year, now.month)[1]
            remaining_days = days_in_month - now.day

            if remaining_days > 0:
                daily_budget = remaining_budget / remaining_days
                print(f"Budget per day: Rs.{daily_budget:.2f}")

    def monthly_report(self):
        expenses = self.load_expenses()

        if not expenses:
            print("\nNo expenses to report!")
            return

        monthly_data = {}
        for expense in expenses:
            month_key = expense.date[:7]
            if month_key not in monthly_data:
                monthly_data[month_key] = []
            monthly_data[month_key].append(expense)

        print("\nMONTHLY EXPENSE REPORT")
        print("=" * 50)

        for month, month_expenses in sorted(monthly_data.items()):
            total = sum(exp.amount for exp in month_expenses)
            print(f"\n{month}: Rs.{total:,.2f} ({len(month_expenses)} transactions)")

            categories = {}
            for exp in month_expenses:
                if exp.category in categories:
                    categories[exp.category] += exp.amount
                else:
                    categories[exp.category] = exp.amount

            for cat, amt in sorted(categories.items()):
                print(f"   {cat}: Rs.{amt:,.2f}")

    def get_current_budget(self):
        budget_file = "farmer_budget.txt"

        if os.path.exists(budget_file):
            try:
                with open(budget_file, 'r', encoding='utf-8') as f:
                    return float(f.read().strip())
            except:
                pass

        return 0

    def set_budget(self):
        current_budget = self.get_current_budget()

        if current_budget > 0:
            print(f"\nCurrent budget: Rs.{current_budget:,.2f}")

        try:
            new_budget = float(input("Enter new monthly budget (Rs.): "))
            if new_budget > 0:
                with open("farmer_budget.txt", 'w', encoding='utf-8') as f:
                    f.write(str(new_budget))
                print(f"Budget set to Rs.{new_budget:,.2f}")
            else:
                print("Budget must be greater than 0!")
        except ValueError:
            print("Please enter a valid number!")

    def run(self):
        self.display_welcome()
        self.main_menu()

def main():
    tracker = FarmerExpenseTracker()
    tracker.run()

if __name__ == "__main__":
    main()
