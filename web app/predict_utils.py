import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the model
model = load_model('./model/model.h5')

# Define a function to preprocess images
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(128, 128))  # Adjust target size according to your model
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

def predict(filename):
    img_path = f'./uploads/{filename}'
    preprocessed_img = preprocess_image(img_path)
    predictions = model.predict(preprocessed_img)
    if(float(predictions[0])>0.5):
        return 0
    return 1
