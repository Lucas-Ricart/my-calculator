import json

history = []  # To store the history of operations

def request_expression():
    """Prompt the user for mathematical expressions to evaluate."""
    global history
    print("Welcome to the advanced calculator!")
    print("Type 'quit' to exit.")
    print("Type 'history' to view history, 'clear history' to clear it, or 'reset history' to reset.")
    while True:
        expression = input("Enter a mathematical expression: ").replace(" ", "")
        
        if expression.lower() == "quit":
            print("Thank you for using the calculator. Goodbye!")
            break

        elif expression.lower() == "history":
            # Show history
            if history:
                print("History of operations:")
                for item in history:
                    print(f"{item['expression']} = {item['result']}")
            else:
                print("No operations in history.")
        
        elif expression.lower() == "clear history":
            # Clear the history
            history = []
            print("History has been cleared.")
        
        elif expression.lower() == "reset history":
            # Reset the history (clear and reload from saved file, if any)
            try:
                with open("history.json", "w") as f:
                    json.dump([], f)
                history = []
                print("History has been reset.")
            except FileNotFoundError:
                print("No saved history to reset.")
        
        else:
            # Simulate calculation and store result in history
            result = f"Result for {expression}"  # Replace with real calculation logic
            history.append({"expression": expression, "result": result})
            print(f"Result: {result}")

            # Optionally, save history to a JSON file
            with open("history.json", "w") as f:
                json.dump(history, f)

if __name__ == "__main__":
    try:
        # Load previous history from the saved file if it exists
        with open("history.json", "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    request_expression()
