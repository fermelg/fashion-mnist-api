import numpy as np
import tensorflow as tf
from tensorflow import keras
import os

class ModelServer:
    def __init__(self, model_path='artifacts/model.h5'):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}.")
        self.model = keras.models.load_model(model_path)
        self.metadata = {
            'model_path': model_path,
            'backend': 'tensorflow',
            'input_shape': (28, 28, 1),
            'num_classes': 10
        }

    def get_metadata(self):
        return self.metadata

    def _validate_payload(self, payload):
        if 'instances' not in payload:
            raise ValueError("Payload must contain 'instances'")
        arr = np.array(payload['instances'])
        return arr

    def preprocess(self, arr):
        arr = arr.astype(np.float32)
        if arr.ndim == 3:
            arr = arr[..., None]
        return arr/255.0

    def postprocess(self, probs):
        classes = np.argmax(probs, axis=1).tolist()
        return {'predictions': classes, 'probabilities': probs.tolist()}

    def predict(self, payload):
        arr = self._validate_payload(payload)
        x = self.preprocess(arr)
        preds = self.model.predict(x)
        return self.postprocess(preds)
