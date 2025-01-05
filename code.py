import os
from datetime import datetime

EXPENSES_FILE = "expenses.txt"

def load_expenses():
    expenses = []
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r") as file:
            for line in file:
                category, amount, date = line.strip().split(",")
                expenses.append({
                    "category": category,
                    "amount": float(amount),
                    "date": datetime.strptime(date, "%Y-%m-%d")
                })
    return expenses

def save_expense(category, amount, date):
    with open(EXPENSES_FILE, "a") as file:
        file.write(f"{category},{amount},{date}\n")

def add_expense():
    category = input("Enter category (e.g., Food, Travel): ").strip()
    try:
        amount = float(input("Enter amount: ").strip())
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        date = datetime.strptime(date_str, "%Y-%m-%d")
        save_expense(category, amount, date_str)
        print("Expense added successfully!\n")
    except ValueError:
        print("Invalid input. Please try again.\n")

def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded.\n")
        return

    expenses_by_category = {}
    for expense in expenses:
        category = expense["category"]
        if category not in expenses_by_category:
            expenses_by_category[category] = []
        expenses_by_category[category].append(expense)

    print("Expenses:")
    for category, items in expenses_by_category.items():
        print(f"{category}:")
        for i, item in enumerate(items, start=1):
            print(f"  {i}. Amount: {item['amount']} - Date: {item['date'].strftime('%Y-%m-%d')}")
    print()

def monthly_summary():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded.\n")
        return

    month = input("Enter month and year (YYYY-MM): ").strip()
    try:
        target_month = datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid input. Please enter in YYYY-MM format.\n")
        return

    monthly_expenses = [
        expense for expense in expenses \
        if expense["date"].year == target_month.year and expense["date"].month == target_month.month
    ]

    if not monthly_expenses:
        print(f"No expenses recorded for {target_month.strftime('%B %Y')}\n")
        return

    total_expenses = sum(expense["amount"] for expense in monthly_expenses)
    expenses_by_category = {}
    for expense in monthly_expenses:
        category = expense["category"]
        expenses_by_category[category] = expenses_by_category.get(category, 0) + expense["amount"]

    print(f"Monthly Summary ({target_month.strftime('%B %Y')}):")
    print(f"Total Expenses: {total_expenses}")
    print("By Category:")
    for category, total in expenses_by_category.items():
        print(f"  {category}: {total}")
    print()

def search_by_date_range():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded.\n")
        return

    try:
        start_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date_str = input("Enter end date (YYYY-MM-DD): ").strip()
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        filtered_expenses = [
            expense for expense in expenses \
            if start_date <= expense["date"] <= end_date
        ]

        if not filtered_expenses:
            print(f"No expenses recorded from {start_date_str} to {end_date_str}.\n")
            return

        total_expenses = sum(expense["amount"] for expense in filtered_expenses)
        expenses_by_category = {}
        for expense in filtered_expenses:
            category = expense["category"]
            expenses_by_category[category] = expenses_by_category.get(category, 0) + expense["amount"]

        print(f"Expenses from {start_date_str} to {end_date_str}:")
        for category, total in expenses_by_category.items():
            print(f"  {category}: {total}")
        print(f"Total Expenses: {total_expenses}\n")
    except ValueError:
        print("Invalid input. Please enter dates in YYYY-MM-DD format.\n")

def main():
    while True:
        print("Welcome to Personal Expense Tracker!")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Search by Date Range")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            search_by_date_range()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
