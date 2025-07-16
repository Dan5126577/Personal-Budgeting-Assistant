import json
from datetime import datetime
import os

DATA_PATH = os.path.join("data", "budget_data.json")

def load_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

def add_expense(amount, category, description):
    data = load_data()
    data["expenses"].append({
        "amount": amount,
        "category": category,
        "description": description,
        "date": str(datetime.now().date())
    })
    save_data(data)

def set_income(amount):
    data = load_data()
    data["income"] = amount
    save_data(data)

def get_summary():
    data = load_data()
    total_expense = sum(item["amount"] for item in data["expenses"])
    remaining = data["income"] - total_expense
    overspending = remaining < 0
    return {
        "income": data["income"],
        "total_expense": total_expense,
        "remaining": remaining,
        "overspending": overspending
    }
