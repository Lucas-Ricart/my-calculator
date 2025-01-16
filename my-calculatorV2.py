import re

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
    print("Welcome to the advanced calculator!")
    print("Type 'quit' to exit.")
    while True:
        expression = input("Enter a mathematical expression: ").replace(" ", "")
        if expression.lower() == "quit":
            print("Thank you for using the calculator. Goodbye!")
            break
        result = calculate(expression)
        print(f"Result: {result}")

if __name__ == "__main__":
    request_expression()
