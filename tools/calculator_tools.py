def calculate(expression):

    try:

        result=eval(expression)

        return result

    except:

        return "Invalid expression"