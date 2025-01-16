import re
import json

history = []  # To store the history of operations

def calculate(expression):
    """Evaluate a mathematical expression with operator precedence and parentheses."""

    def apply_operation(op, a, b):
        """Apply a mathematical operation between two numbers."""
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ValueError("Division by zero is not allowed.")
            return a / b
        elif op == '^':
            return a ** b

    def evaluate_simple(expression):
        """Evaluate an expression without parentheses, respecting operator precedence."""
        priorities = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}
        numbers = []
        operators = []

        i = 0
        while i < len(expression):
            if expression[i].isdigit() or expression[i] == '.':  # Read a number
                number = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number += expression[i]
                    i += 1
                numbers.append(float(number))
                continue

            elif expression[i] == '-' and (i == 0 or expression[i-1] in "+-*/^("):
                # Handle negative numbers
                number = "-"
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number += expression[i]
                    i += 1
                numbers.append(float(number))
                continue

            elif expression[i] in priorities:  # Read an operator
                while (operators and 
                       priorities[operators[-1]] >= priorities[expression[i]]):
                    op = operators.pop()
                    b = numbers.pop()
                    a = numbers.pop()
                    numbers.append(apply_operation(op, a, b))
                operators.append(expression[i])
            
            i += 1

        # Apply remaining operators
        while operators:
            op = operators.pop()
            b = numbers.pop()
            a = numbers.pop()
            numbers.append(apply_operation(op, a, b))

        return numbers[0]

    def evaluate(expression):
        """Evaluate an expression, processing parentheses first."""
        while '(' in expression:
            # Find the innermost parentheses
            match = re.search(r'\(([^()]+)\)', expression)
            if match:
                sub_expression = match.group(1)
                result = evaluate_simple(sub_expression)
                expression = expression.replace(f'({sub_expression})', str(result))
        return evaluate_simple(expression)

    try:
        return evaluate(expression)
    except Exception as e:
        return f"Error: {e}"

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
            result = calculate(expression)
            # Store the result in history
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
