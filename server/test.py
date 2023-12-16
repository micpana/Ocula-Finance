from flask import Flask, request, send_file, jsonify, make_response
import threading
import time
from test2 import run_predictions

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['POST', 'GET'])
def index():
    response = make_response('Not authorized')
    response.status = 401
    
    # return response
    return response

# Create and start the prediction thread
prediction_thread = threading.Thread(target=run_predictions)

# Start the prediction thread if not already running
if not prediction_thread.is_alive():
    prediction_thread.start()
else:
    print('prediction thread already running')

if __name__ == '__main__':
    app.run(host='0.0.0.0')