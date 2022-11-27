import tensorflow as tf


class ModelLoader:
    def __init__(self, path: str, name: str, backend="tensorflow"):
        self.backend = backend
        self.name = name
        self.path = path

        if self.backend == "tensorflow":
            self.model = self.__load_model_from_tensorflow(self.path)
        else:
            raise NotImplementedError

    def __load_model_from_tensorflow(self, model_path):
        print("Loading model from tensorflow")
        self.model = tf.keras.models.load_model(model_path)
        print("Model loaded")
        return self.model

    def predict(self, data):
        return self.model.predict(data)

    def __call__(self, data):
        return self.predict(data)  # this is the same as the predict method
