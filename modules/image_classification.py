import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from keras.preprocessing.image import img_to_array
from PIL import Image
import cv2
import numpy as np

# Load model once to prevent multiple initializations
model = MobileNetV2(weights="imagenet")

nature_keywords = [
    "beach", "coast", "mountain", "forest", "valley", "lake",
    "sea", "ocean", "tree", "field", "cliff", "sky", "landscape", "desert"
]

def is_nature_image(image_path):
    """Check if an image is a nature photo."""
    try:
        image = Image.open(image_path).convert("RGB")
        image = image.resize((224, 224))
        image_array = img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array = preprocess_input(image_array)

        predictions = model.predict(image_array)
        decoded_predictions = decode_predictions(predictions, top=5)[0]

        for _, label, _ in decoded_predictions:
            if any(keyword in label.lower() for keyword in nature_keywords):
                return True
        return False
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

def is_non_photo(image_path):
    """Check if the image is likely a non-photo."""
    try:
        image = cv2.imread(image_path, 0)
        edges = cv2.Canny(image, 100, 200)
        edge_density = np.mean(edges)
        return edge_density > 0.3
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False
