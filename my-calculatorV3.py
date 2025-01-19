import re
import json
from decimal import *

getcontext().prec = 16
history = {}  # To store the history of operations
reset_history = {}
count = 1

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
                numbers.append(Decimal(number))
                continue

            elif expression[i] == '-' and (i == 0 or expression[i-1] in "+-*/^("):
                # Handle negative numbers
                number = "-"
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number += expression[i]
                    i += 1
                numbers.append(Decimal(number))
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

def request_expression(history, reset_history, count):
    """Prompt the user for mathematical expressions to evaluate."""
    print("Welcome to the advanced calculator!")
    while True:
        print("Type 'quit' to exit.")
        print("Type 'history' to view history, 'clear history' to clear it, or 'reset history' to reset.")
        expression = input("Enter a mathematical expression: ").replace(" ", "")
        
        if expression.lower() == "quit":
            print("Thank you for using the calculator. Goodbye!")
            break

        elif expression.lower() == "history":
            # Show history
            if history:
                print("History of operations:")
                for item in history:
                    print(history[item])
            else:
                print("No operations in history.")
        
        elif expression.lower() == "clear":
            # Clear the history
            count = 1
            history = {}
            with open("history.json", "w") as f:
                    json.dump(history, f)
            print("History has been cleared.")
        
        elif expression.lower() == "reset":
            # Reset the history (clear and reload from saved file, if any)
            try:
                with open("history.json", "w") as f:
                    json.dump(reset_history, f)
                with open("history.json", "r") as f:
                    history = json.load(f)
                count = 1
                for item in history :
                    count +=1
                print("History has been reset.")
            except FileNotFoundError:
                print("No saved history to reset.")
        
        else:
            result = calculate(expression)
            print(f"Result: {result}")
            result = str(result)
            if "Error" in result :
                None
            else :
                # Store the result in history
                counts = str(count)
                history["calcul"+counts] = ({"expression": expression, "result": result})
                count += 1
                

            # Optionally, save history to a JSON file
            with open("history.json", "w") as f:
                json.dump(history, f)

if __name__ == "__main__":
    try:
        # Load previous history from the saved file if it exists
        with open("history.json", "r") as f:
            history = json.load(f)
        with open("history.json", "r") as f:
            reset_history = json.load(f)
        for item in history :
            count +=1
    except (FileNotFoundError, json.JSONDecodeError):
        None

    request_expression(history, reset_history, count)
