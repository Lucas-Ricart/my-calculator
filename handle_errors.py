def handle_errors(expression, evaluate):
    """Handle errors during evaluation of a mathematical expression."""
    try:
        return evaluate(expression)
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except Exception as e:
        return f"Error: {e}"
