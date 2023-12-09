import traceback

try:
    exec(loaded_data['code'])
except Exception as e:
    print('Prediction Code Execution Error')

    # print the type of exception and a custom message
    print(f"An exception of type {type(e).__name__} occurred: {str(e)}")

    # print the traceback details
    traceback.print_exc()