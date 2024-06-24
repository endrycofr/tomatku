import streamlit as st
from PIL import Image
import io
import numpy as np
import tensorflow as tf
from keras.utils import img_to_array, load_img
import os

# Load TFLite model with caching
@st.cache_resource
def load_tflite_model(path):
    try:
        interpreter = tf.lite.Interpreter(model_path=path)
        interpreter.allocate_tensors()
        print("TFLite model loaded successfully.")
        return interpreter
    except Exception as e:
        print(f"Failed to load TFLite model: {e}")
        return None

# Treatment suggestions
def get_treatment(prediction):
    treatments = {
        'Healthy': 'No treatment is needed as the plant is healthy. Maintain regular care and monitoring.',
        'Powdery': (
            "<ul>"
            "<li>Remove and destroy affected plant parts.</li>"
            "<li>Apply fungicides such as sulfur or potassium bicarbonate.</li>"
            "<li>Ensure good air circulation around plants.</li>"
            "<li>Avoid overhead watering.</li>"
            "</ul>"
        ),
        'Rust': (
            "<ul>"
            "<li>Remove and destroy affected leaves.</li>"
            "<li>Apply fungicides like neem oil or copper-based sprays.</li>"
            "<li>Water plants at the base to avoid wetting the leaves.</li>"
            "<li>Ensure proper spacing for good air circulation.</li>"
            "</ul>"
        )
    }
    return treatments.get(prediction, "No treatment information available.")

# Descriptions for each label
def get_description(prediction):
    descriptions = {
        'Healthy': (
            "<p>The plant is in good condition with no signs of disease or pests. Healthy leaves are typically vibrant in color, free from spots or discoloration, and have a normal, consistent texture. Proper care involves regular watering, adequate sunlight, and occasional fertilization.</p>"
        ),
        'Powdery': (
            "<p>Powdery mildew is a fungal disease that affects a wide range of plants. It is characterized by white or gray powdery spots on the leaves and stems. These spots can eventually cause the leaves to yellow, curl, or drop prematurely. Conditions that favor powdery mildew include high humidity and poor air circulation. Regular monitoring and proper treatment can help manage and control this disease.</p>"
        ),
        'Rust': (
            "<p>Rust is a common fungal disease that causes orange, yellow, or brown spots on the undersides of leaves. Over time, these spots may develop into pustules that release spores, spreading the infection. Rust can weaken plants, reducing their vigor and productivity. It thrives in wet, humid conditions and is often spread by wind and water. Early detection and treatment are essential to prevent severe infestations.</p>"
        )
    }
    return descriptions.get(prediction, "No description information available.")

# Image Processing
def process_image(img_path):
    img = load_img(img_path, target_size=(225, 225))  # Resize image to match model input shape
    img = img_to_array(img)
    img = img / 255.0  # Normalize to [0, 1]
    img = np.expand_dims(img, axis=0)
    return img

def get_tflite_prediction(interpreter, image):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])
    prediction_index = np.argmax(predictions)
    prediction_label = labels[prediction_index]
    return prediction_label, predictions

# Load TFLite Model
tflite_model_path = 'model2.tflite'
interpreter = load_tflite_model(tflite_model_path)
if interpreter is None:
    st.stop()

# Labels mapping
labels = {0: 'Healthy', 1: 'Powdery', 2: 'Rust'}

# Streamlit Interface
st.title('Plant Disease Detection')
st.write("Upload your plant's leaf image and get predictions on whether the plant is healthy or not.")

uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

# Ensure the images directory exists
os.makedirs('./images', exist_ok=True)

if uploaded_file is not None:
    try:
        # Display image
        image = Image.open(io.BytesIO(uploaded_file.read()))
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Save Image
        img_path = os.path.join('./images', uploaded_file.name)
        with open(img_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Process Image
        processed_img = process_image(img_path)

        # Get Prediction
        prediction_label, predictions = get_tflite_prediction(interpreter, processed_img)

        # Display Results with Styling
        status_html = f'<span style="color:green; font-weight:bold;">The plant is {prediction_label}</span>'
        prediction_html = f'<span style="color:blue; font-weight:bold;">Prediction: {prediction_label}</span>'
        
        st.markdown(f'<div style="text-align:center; font-size:24px;">{status_html}<br>{prediction_html}</div>', unsafe_allow_html=True)
        
        # Fetch and Display Description
        description_html = get_description(prediction_label)
        st.markdown(description_html, unsafe_allow_html=True)
        
        # Fetch and Display Treatment
        treatment_html = get_treatment(prediction_label)
        st.markdown(f'<div style="background-color: rgba(135, 206, 235, 0.1); padding: 20px; border-radius: 5px; font-size: 18px;"><p>Treatment:</p>{treatment_html}</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please upload an image to get started.")


