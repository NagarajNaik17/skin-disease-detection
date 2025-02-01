import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Load the saved model and label mappings
model = tf.keras.models.load_model("saved_model/skin_disease_model.h5")
label_map = np.load("saved_model/label_map.npy", allow_pickle=True).item()
inverse_label_map = np.load("saved_model/inverse_label_map.npy", allow_pickle=True).item()

def predict(image_path):
    img_height, img_width = 128, 128
    img = load_img(image_path, target_size=(img_height, img_width))
    img_array = img_to_array(img) / 255.0  # Normalize to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = predictions[0][predicted_class]

    disease_name = inverse_label_map[predicted_class]
    return disease_name, confidence

# Example usage
image_path = "static/image1.jpg.jpg"  # Replace with the uploaded image path
disease, confidence = predict(image_path)
print(f"Predicted: {disease} with {confidence:.2f} confidence")
