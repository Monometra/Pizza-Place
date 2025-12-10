import sys
from functions import (
    MENUS, display_menu, calculate_total, clear_screen, 
    save_order, get_total_revenue
)

def handle_menu_selection(title, menu_dict, order):
    """
    Handles the display and selection logic for any menu.
    Allows multiple selections and prompts to add another.
    """
    # Optimization: Cache the list of items to avoid recreating it in the loop
    items_list = list(menu_dict.values())
    
    while True:
        display_menu(title, menu_dict)
        item = input("Select item by number (or 'back' to return): ").strip()
        if item.lower() == "back":
            break
        try:
            num = int(item)
            if 1 <= num <= len(items_list):
                selected_item = items_list[num - 1]
                order.append(selected_item)
                print(f"Added {selected_item.name} to order.")
                
                # UX Improvement: Ask if user wants to add another item
                while True:
                    add_another = input("Add another item? (y/n): ").strip().lower()
                    if add_another == 'y':
                        break  # Continue the outer loop to show menu again
                    elif add_another == 'n':
                        return  # Exit the function and return to main menu
                    else:
                        print("Please enter 'y' or 'n'.")
            else:
                print("Invalid number.")
                input("Press Enter to continue...")
        except ValueError:
            print("Invalid input.")
            input("Press Enter to continue...")

def main():
    """Main execution loop for the Pizza Place Business System."""
    order = []
    while True:
        clear_screen()
        print("Pizza Palace v1.0")
        print("""
┌──────────────────────────────────────┐
│        WELCOME TO PIZZA PALACE       │
└──────────────────────────────────────┘
        """)
        print("1. Pizzas")
        print("2. Panzerottis")
        print("3. Drinks")
        print("4. Additionals")
        print("5. View Order")
        print("6. Checkout")
        print("7. Exit")
        choice = input("Choose an option: ").strip()
        if choice in MENUS:
            title, menu_dict = MENUS[choice]
            handle_menu_selection(title, menu_dict, order)
        elif choice == "5":
            clear_screen()
            print("""
┌──────────────────────────────────────┐
│             YOUR ORDER               │
└──────────────────────────────────────┘
            """)
            if not order:
                print("No items in order.")
            else:
                for item in order:
                    print(item)
                print(f"\nTotal: ${calculate_total(order):.2f}")
            input("Press Enter to continue...")
        elif choice == "6":
            clear_screen()
            print("""
┌──────────────────────────────────────┐
│              CHECKOUT                │
└──────────────────────────────────────┘
            """)
            if not order:
                print("No items in order.")
                input("Press Enter to continue...")
                continue
            for item in order:
                print(item)
            total = calculate_total(order)
            print(f"\nTotal: ${total:.2f}")
            try:
                customer_name = input("Enter customer name: ").strip()
                if not customer_name:
                    customer_name = "Anonymous"
                payment_input = input("Enter payment amount: ").strip()
                # Input Sanitization: Remove '$' if present
                payment_input = payment_input.replace('$', '')
                payment = float(payment_input)
                
                if payment >= total:
                    print(f"Change: ${payment - total:.2f}")
                    
                    # Save order using new function
                    try:
                        order_id, current_time = save_order(order, customer_name, total)
                        
                        print(f"Date: {current_time}")
                        print(f"Order ID: {order_id}")
                        print(f"Customer: {customer_name}")
                        print("Thank you for your order!")
                        
                    except Exception as e:
                        print(f"Error logging order: {e}")
                    
                    # Checkout Flow Improvement: Ask to process another order
                    while True:
                        another_order = input("Process another order? (y/n): ").strip().lower()
                        if another_order == 'y':
                            order = []  # Reset order for new customer
                            break # Break inner loop, go back to main menu loop
                        elif another_order == 'n':
                            # Print exit summary using new function
                            total_rev, count = get_total_revenue()
                            print(f"Total orders processed: {count}")
                            print(f"Total Revenue: ${total_rev:.2f}")
                            print("Goodbye!")
                            return # Exit the program
                        else:
                            print("Please enter 'y' or 'n'.")
                    
                    # If we broke the inner loop, we continue the main loop
                    continue 
                    
                else:
                    print("Insufficient payment.")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid payment amount.")
                input("Press Enter to continue...")
        elif choice == "7":
            # Print exit summary using new function
            total_rev, count = get_total_revenue()
            print(f"Total orders processed: {count}")
            print(f"Total Revenue: ${total_rev:.2f}")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()