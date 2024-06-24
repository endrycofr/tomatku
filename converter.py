import tensorflow as tf

# Path to the Keras model
model_path = 'model2.h5'
tflite_model_path = 'model2.tflite'

# Load the Keras model
model = tf.keras.models.load_model(model_path)

# Convert the model to TFLite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model
with open(tflite_model_path, 'wb') as f:
    f.write(tflite_model)

print(f"TFLite model saved to {tflite_model_path}")
