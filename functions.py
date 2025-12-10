import os
import json
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MenuItem:
    """Represents a single menu item with a name and price."""
    name: str
    price: float
    def get_display(self):
        """Returns a formatted string for display in the menu."""
        return f"{self.name} ${self.price:.2f}"
    def __str__(self):
        return f"{self.name}: ${self.price:.2f}"
    
    # Add to_dict for JSON serialization
    def to_dict(self):
        return {"name": self.name, "price": self.price}

# Global variables for menus using MenuItem class
PIZZA_MENU = {
    "Margherita": MenuItem("Margherita", 12.99),
    "Pepperoni": MenuItem("Pepperoni", 14.99),
    "Hawaiian": MenuItem("Hawaiian", 15.99),
    "Veggie": MenuItem("Veggie", 13.99),
}

PANZEROTTI_MENU = {
    "Cheese": MenuItem("Cheese", 8.99),
    "Meat": MenuItem("Meat", 10.99),
    "Spinach": MenuItem("Spinach", 9.99),
}

DRINK_MENU = {
    "Coke": MenuItem("Coke", 2.99),
    "Sprite": MenuItem("Sprite", 2.99),
    "Water": MenuItem("Water", 1.99),
    "Beer": MenuItem("Beer", 4.99),
}

ADDITIONAL_MENU = {
    "Extra Cheese": MenuItem("Extra Cheese", 2.00),
    "Garlic Bread": MenuItem("Garlic Bread", 3.99),
    "Salad": MenuItem("Salad", 5.99),
}

# Consolidated menu structure for easy access
MENUS = {
    "1": ("PIZZA MENU", PIZZA_MENU),
    "2": ("PANZEROTTI MENU", PANZEROTTI_MENU),
    "3": ("DRINK MENU", DRINK_MENU),
    "4": ("ADDITIONAL MENU", ADDITIONAL_MENU),
}

def display_menu(title, menu_dict):
    """Displays the menu options in a formatted box."""
    width = 40
    print("┌" + "─" * (width - 2) + "┐")
    print("│" + title.center(width - 2) + "│")
    print("├" + "─" * (width - 2) + "┤")
    for i, item in enumerate(menu_dict.values(), 1):
        prefix = f" {i}. "
        price_part = f"${item.price:.2f} "
        
        max_name_len = width - 2 - len(prefix) - len(price_part)
        
        display_name = item.name
        if len(display_name) > max_name_len:
            display_name = display_name[:max_name_len-3] + "..."
            
        spaces_needed = width - 2 - len(prefix) - len(display_name) - len(price_part)
        spaces_needed = max(0, spaces_needed)
        
        print(f"│{prefix}{display_name}{' ' * spaces_needed}{price_part}│")
    print("└" + "─" * (width - 2) + "┘")

def calculate_total(order):
    """Calculates the total price of the order."""
    return sum(item.price for item in order)

def clear_screen():
    """Clears the terminal screen with a fallback for compatibility."""
    try:
        if os.name == "nt":
            os.system("cls")
        else:
            print('\033[2J\033[H', end='')
    except Exception:
        print('\n' * 50)

def get_database_path():
    """Returns the path to the orders database file."""
    # Assumes database directory is in the same directory as this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "database", "orders.json")

def save_order(order, customer_name, total):
    """Saves the order to the JSON database."""
    db_path = get_database_path()
    
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    order_id = now.strftime("%Y%m%d%H%M%S")
    
    order_data = {
        "order_id": order_id,
        "timestamp": current_time,
        "customer_name": customer_name,
        "items": [item.to_dict() for item in order],
        "total": total
    }
    
    orders = []
    if os.path.exists(db_path):
        try:
            with open(db_path, "r") as f:
                orders = json.load(f)
        except json.JSONDecodeError:
            orders = [] # Start fresh if corrupt
            
    orders.append(order_data)
    
    with open(db_path, "w") as f:
        json.dump(orders, f, indent=4)
        
    return order_id, current_time

def get_total_revenue():
    """Calculates total revenue from the JSON database."""
    db_path = get_database_path()
    if not os.path.exists(db_path):
        return 0.0, 0
        
    try:
        with open(db_path, "r") as f:
            orders = json.load(f)
            
        total_revenue = sum(order.get("total", 0) for order in orders)
        count = len(orders)
        return total_revenue, count
    except (json.JSONDecodeError, Exception):
        return 0.0, 0
