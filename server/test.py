import traceback

try:
    # Your code that may raise an exception
    result = 10 / 'a'
except Exception as e:
    # Print the type of exception and a custom message
    print(f"An exception of type {type(e).__name__} occurred: {str(e)}")

    # Print the traceback details
    traceback.print_exc()
