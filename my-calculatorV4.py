import re
import json

# Constants for mathematical calculations
PI = 3.141592653589793
E = 2.718281828459045

# Initialize history
history = {}
count = 1

# Functions for mathematical operations
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)

def sin(x):
    x = x % (2 * PI)
    result, term, n = x, x, 1
    while abs(term) > 1e-10:
        term *= -x**2 / ((2 * n) * (2 * n + 1))
        result += term
        n += 1
    return result

def cos(x):
    x = x % (2 * PI)
    result, term, n = 1, 1, 1
    while abs(term) > 1e-10:
        term *= -x**2 / ((2 * n - 1) * (2 * n))
        result += term
        n += 1
    return result

def tan(x):
    cos_val = cos(x)
    if abs(cos_val) < 1e-10:
        return "Error: tan undefined for this input"
    return sin(x) / cos_val

def exp(x):
    result, term, n = 1, 1, 1
    while term > 1e-10:
        term *= x / n
        result += term
        n += 1
    return result

def ln(x):
    if x <= 0:
        return "Error: ln of non-positive value"
    z = (x - 1) / (x + 1)
    term, result, n = z, 0, 1
    while abs(term) > 1e-10:
        result += term / n
        term *= z * z
        n += 2
    return 2 * result

def log(x):
    return ln(x) / ln(10)

# Function to evaluate mathematical expressions
def calculate(expression):
    def evaluate_function(expression):
        match = re.search(r'([a-z]+)\(([^()]+)\)', expression)
        if match:
            func, value = match.groups()
            value = float(evaluate(value))  # Recursively evaluate the inner value
            if func == 'sin':
                result = sin(value)
            elif func == 'cos':
                result = cos(value)
            elif func == 'tan':
                result = tan(value)
            elif func == 'ln':
                result = ln(value)
            elif func == 'log':
                result = log(value)
            elif func == 'exp':
                result = exp(value)
            else:
                return f"Error: Unknown function '{func}'"
            return expression.replace(f'{func}({value})', str(result))
        return expression

    def evaluate(expression):
        expression = re.sub(r'\bpi\b', str(PI), expression)
        expression = re.sub(r'\be\b', str(E), expression)
        expression = re.sub(r'(\d)\(', r'\1*(', expression)
        expression = expression.replace("^", "**")  # Replace `^` with `**` for power
        expression = evaluate_function(expression)
        return eval(expression)

    try:
        return evaluate(expression)
    except Exception as e:
        return f"Error: {e}"

# Format result to remove trailing decimal if it's unnecessary
def format_result(result):
    if isinstance(result, float):
        if result.is_integer():
            return int(result)  # Remove decimal point if the number is an integer
        else:
            return result  # Keep as float if it's not an integer
    return result  # Return as is if it's not a number

# Main interaction loop
def request_expression(history, count):
    """Prompt the user for mathematical expressions to evaluate."""
    print("Welcome to the advanced calculator!")
    print("Type 'quit' to exit.")
    print("Type 'history' to view history, 'clear' to clear history, or 'reset' to reset.")

    while True:
        expression = input("Enter a mathematical expression: ").replace(" ", "")

        if expression.lower() == "quit":
            print("Thank you for using the calculator. Goodbye!")
            break

        elif expression.lower() == "history":
            if history:
                print("History of operations:")
                item = {}
                for item in history:
                    for expression, result in history[item].items() :
                        print(expression,'=',result)
            else:
                print("No operations in history.")

        elif expression.lower() == "clear":
            history.clear()
            with open("history.json", "w") as f:
                json.dump(history, f)
            print("History has been cleared.")

        elif expression.lower() == "reset":
            if history:
                last_key = list(history.keys())[-1]  # Get the last operation key
                del history[last_key]  # Remove the last operation
                with open("history.json", "w") as f:
                    json.dump(history, f)
                print(f"Last operation ({last_key}) has been removed from history.")
            else:
                print("No history to reset.")

        else:
            result = calculate(expression)
            formatted_result = format_result(result)
            print(f"Result: {formatted_result}")

            if not isinstance(result, str) or not result.startswith("Error"):
                key = f"Calcul{count}"
                history[key] = {"Expression": expression, "Result": str(formatted_result)}
                count += 1
                with open("history.json", "w") as f:
                    json.dump(history, f)

# Entry point
if __name__ == "__main__":
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
        count = len(history) + 1
    except (FileNotFoundError, json.JSONDecodeError):
        history = {}

    request_expression(history, count)
