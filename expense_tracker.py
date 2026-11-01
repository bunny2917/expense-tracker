"""
Project Name: Smart Expense Tracker & Financial Visualizer
Tech Stack: Python, Pandas, Matplotlib, CSV

Description:
A comprehensive personal finance CLI tool that tracks daily income and expenses,
categorizes transactions, computes monthly summaries, and generates visual analytics 
charts (pie charts for category distribution and bar charts for monthly trends).
"""

import os
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "expenses.csv"

def init_file():
    """Initializes the CSV file with headers if it doesn't already exist."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Type", "Category", "Amount", "Description"])

def add_transaction():
    """Takes input for a new transaction (Income/Expense)."""
    print("\n--- Add Transaction ---")
    trans_type = input("Type (Expense/Income) [Default: Expense]: ").strip().capitalize()
    if trans_type not in ["Expense", "Income"]:
        trans_type = "Expense"

    date_input = input("Date (YYYY-MM-DD) [Leave empty for today]: ").strip()
    if not date_input:
        date_input = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Using today's date.")
            date_input = datetime.now().strftime("%Y-%m-%d")

    category = input("Category (e.g., Food, Travel, Gym, Study, Shopping): ").strip().title()
    if not category:
        category = "Other"

    try:
        amount = float(input("Amount (INR): ").strip())
    except ValueError:
        print("Invalid amount! Transaction cancelled.")
        return

    desc = input("Note / Description: ").strip()

    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([date_input, trans_type, category, amount, desc])

    print(" Transaction logged successfully!")

def view_summary():
    """Displays a tabular summary of transactions using Pandas."""
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        print("\nNo data found! Add transactions first.")
        return

    df = pd.read_csv(DATA_FILE)
    if df.empty:
        print("\nNo transactions available.")
        return

    print("\n" + "="*60)
    print("                    FINANCIAL SUMMARY")
    print("="*60)
    print(df.to_string(index=False))
    print("-" * 60)

    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
    net_savings = total_income - total_expense

    print(f"Total Income   : ₹{total_income:,.2f}")
    print(f"Total Expenses : ₹{total_expense:,.2f}")
    print(f"Net Savings    : ₹{net_savings:,.2f}")
    print("="*60)

def generate_analytics():
    """Generates visual expenditure charts using Matplotlib."""
    if not os.path.exists(DATA_FILE):
        print("\nNo transaction history to plot.")
        return

    df = pd.read_csv(DATA_FILE)
    expense_df = df[df["Type"] == "Expense"]

    if expense_df.empty:
        print("\nNo expenses recorded yet to plot charts.")
        return

    cat_group = expense_df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(10, 5))

    # 1. Category Pie Chart
    plt.subplot(1, 2, 1)
    cat_group.plot(kind='pie', autopct='%1.1f%%', startangle=140, cmap='Set2')
    plt.title("Expense Breakdown by Category")
    plt.ylabel("")

    # 2. Category Bar Chart
    plt.subplot(1, 2, 2)
    cat_group.plot(kind='bar', color='#4CAF50')
    plt.title("Total Spend per Category (₹)")
    plt.xlabel("Category")
    plt.ylabel("Amount in INR")
    plt.xticks(rotation=45)

    plt.tight_layout()
    chart_filename = "spending_analytics.png"
    plt.savefig(chart_filename)
    print(f"\n Analytics chart generated and saved as '{chart_filename}'!")
    plt.show()

def main_menu():
    init_file()
    while True:
        print("\n" + "="*35)
        print("   SMART EXPENSE TRACKER (PYTHON)")
        print("="*35)
        print("1. Add Income / Expense")
        print("2. View All Transactions & Balance")
        print("3. Generate Analytics & Charts")
        print("4. Exit")
        choice = input("\nEnter choice (1-4): ").strip()

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            generate_analytics()
        elif choice == '4':
            print("\nExiting... Have a productive day!")
            break
        else:
            print("Invalid selection! Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main_menu()
