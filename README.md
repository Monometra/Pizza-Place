# Pizza Place Business System

## Description

A robust terminal-based application designed to streamline operations for a pizza restaurant. This system handles the entire order lifecycle, from menu browsing and item selection to checkout and data persistence. It features a modular architecture and uses a JSON database for reliable record-keeping.

## Features

- **Interactive Menu System**: Easy-to-navigate menus for Pizzas, Panzerottis, Drinks, and Additional items.
- **Order Management**: Real-time order building with the ability to view and modify selections before checkout.
- **Data Persistence**: All orders are automatically saved to a structured JSON database, ensuring no data is lost.
- **Revenue Tracking**: Built-in functionality to calculate and display total revenue and order counts.
- **Input Validation**: Robust handling of user inputs to prevent crashes and ensure data integrity.

## Project Structure

- **pizza.py**: The main entry point of the application. Handles the user interface and application flow.
- **functions.py**: Contains the core business logic, data models, and helper functions.
- **database/**: Directory containing the JSON database files.
    - **orders.json**: Stores the history of all processed orders.

## Requirements

- Python 3.6 or higher

## Usage

1. Open your terminal or command prompt.
2. Navigate to the project directory.
3. Run the application using the following command:

   ```bash
   python pizza.py
   ```

4. Follow the on-screen prompts to navigate the menu and process orders.
