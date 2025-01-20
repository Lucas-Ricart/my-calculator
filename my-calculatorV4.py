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
    # Convert degrees to radians
    x = x % 360  # Normalize angle
    x = x * PI / 180
    result, term, n = x, x, 1
    while abs(term) > 1e-10:
        term *= -x**2 / ((2 * n) * (2 * n + 1))
        result += term
        n += 1
    return result

def cos(x):
    # Convert degrees to radians
    x = x % 360  # Normalize angle
    x = x * PI / 180
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

def sqrt(x):
    if x < 0:
        return "Error: Cannot compute square root of a negative number"
    guess, epsilon = x / 2, 1e-10
    while abs(guess * guess - x) > epsilon:
        guess = (guess + x / guess) / 2
    return guess

# Function to evaluate mathematical expressions manually (without eval())
def calculate(expression):
    def handle_functions(expression):
        """ Handle functions like sin(), cos(), etc. """
        functions = ['sin', 'cos', 'tan', 'exp', 'ln', 'log', 'sqrt']
        for func in functions:
            expression = re.sub(rf'{func}\(([^)]+)\)', lambda m: str(evaluate_function(func, m.group(1))), expression)
        return expression

    def evaluate_function(func, value):
        """ Evaluate a single mathematical function call. """
        value = float(calculate(value))  # Recursively evaluate the inner value
        if func == 'sin':
            return sin(value)
        elif func == 'cos':
            return cos(value)
        elif func == 'tan':
            return tan(value)
        elif func == 'exp':
            return exp(value)
        elif func == 'ln':
            return ln(value)
        elif func == 'log':
            return log(value)
        elif func == 'sqrt':
            return sqrt(value)

    def evaluate(expression):
        expression = re.sub(r'\bpi\b', str(PI), expression)
        expression = re.sub(r'\be\b', str(E), expression)
        expression = re.sub(r'(\d)\(', r'\1*(', expression)  # Handle cases like 3(4+5)
        expression = expression.replace("^", "**")  # Replace `^` with `**` for power
        return expression

    def process_operations(expression):
        """ Manually process arithmetic operations respecting the order of operations. """
        # Step 1: Handle exponentiation (**)
        while '**' in expression:
            expression = re.sub(r'(\d+\.\d+|\d+)\*\*(\d+\.\d+|\d+)', lambda m: str(float(m.group(1)) ** float(m.group(2))), expression)

        # Step 2: Handle multiplication (*) and division (/)
        while '*' in expression or '/' in expression:
            expression = re.sub(r'(\d+\.\d+|\d+)\s*([\*/])\s*(\d+\.\d+|\d+)', lambda m: str(compute(m.group(1), m.group(2), m.group(3))), expression)

        # Step 3: Handle addition (+) and subtraction (-)
        while '+' in expression or '-' in expression:
            expression = re.sub(r'(\d+\.\d+|\d+)\s*([+-])\s*(\d+\.\d+|\d+)', lambda m: str(compute(m.group(1), m.group(2), m.group(3))), expression)

        return expression

    def compute(left, operator, right):
        """ Perform arithmetic operations (+, -, *, /). """
        left, right = float(left), float(right)
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left / right

    # Evaluate and process the expression
    expression = handle_functions(expression)
    expression = evaluate(expression)
    return process_operations(expression)

# Format result to remove trailing decimal if unnecessary
def format_result(result):
    try:
        result = float(result)
        if result.is_integer():
            return int(result)  # Remove decimal point if the number is an integer
        return result
    except ValueError:
        return result

# Main interaction loop
def request_expression(history, count):
    """Prompt the user for mathematical expressions to evaluate."""
    print("Welcome to the calculator! Type 'quit' to exit.")
    print("Type 'history' to view history, 'clear' to clear history, or 'reset' to reset.")

    while True:
        expression = input("Enter a mathematical expression: ").replace(" ", "")

        if expression.lower() == "quit":
            print("Goodbye!")
            break

        elif expression.lower() == "history":
            if history:
                print("History of operations:")
                for key, value in history.items():
                    print(f"{key}: {value['Expression']} = {value['Result']}")
            else:
                print("No operations in history.")

        elif expression.lower() == "clear":
            history.clear()
            print("History cleared.")

        elif expression.lower() == "reset":
            if history:
                last_key = list(history.keys())[-1]
                del history[last_key]
                print(f"Last operation ({last_key}) removed.")
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

# Entry point
if __name__ == "__main__":
    request_expression(history, count)
