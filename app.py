from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the trained model
model = load_model('final_model.keras')

# Define the list of classes corresponding to the diseases
classes = [
    'Cold sores',         # Index 0
    'Ichthyosis',         # Index 1
    'Ringworm',           # Index 2
    'Vitiligo',           # Index 3
    'Acne',               # Index 4
    'Eczema',             # Index 5
    'Psoriasis'           # Index 6
]

# Map classes to HTML files
class_to_html = {
    'Cold sores': 'cold_sores.html',
    'Ichthyosis': 'ichthyosis.html',
    'Ringworm': 'ringworm.html',
    'Vitiligo': 'vitiligo.html',
    'Acne': 'acne.html',
    'Eczema': 'eczema.html',
    'Psoriasis': 'psoriasis.html'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part in the request."
        
        file = request.files['file']
        if file.filename == '':
            return "No selected file."

        if file and file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
            # Generate a unique filename to avoid conflicts
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            img_path = os.path.join("static", unique_filename)
            file.save(img_path)

            # Preprocess the image
            img = load_img(img_path)
            img = img.resize((128, 128))
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Make prediction
            prediction = model.predict(img_array)
            predicted_class = classes[np.argmax(prediction)]
            confidence = np.max(prediction)

            # Get the corresponding HTML file for the predicted class
            prescription_html = class_to_html.get(predicted_class, None)

            return render_template(
                'index.html',
                predicted_class=predicted_class,
                confidence=f"{confidence:.2f}",
                prescription_html=prescription_html,
                img_path=img_path  # Pass the image path to the template
            )
        else:
            return "Error: Please upload a valid image file."

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
