from flask import Flask, request, jsonify
from model_server import ModelServer
import logging
import time

app = Flask(__name__)
model = ModelServer("artifacts/model.h5")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status':'ok'}), 200

@app.route('/metadata', methods=['GET'])
def metadata():
    return jsonify(model.get_metadata())

@app.route('/predict', methods=['POST'])
def predict():
    start = time.time()
    try:
        data = request.get_json(force=True)
    except Exception as e:
        return jsonify({'error':'invalid json', 'detail': str(e)}), 400
    try:
        result = model.predict(data)
    except ValueError as e:
        return jsonify({'error':'bad request', 'detail': str(e)}), 400
    except Exception as e:
        logging.exception("Prediction failed")
        return jsonify({'error':'internal server error'}), 500
    latency = (time.time() - start) * 1000
    logging.info(f"predict latency={latency:.2f}ms")
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
