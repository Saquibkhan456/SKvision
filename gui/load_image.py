import numpy as np
from PIL import Image

def load_image(filepath):
    if filepath.endswith(".npy"):
        return np.load(filepath)
    elif filepath.endswith((".jpg", ".png")):
        img = Image.open(filepath)
        return np.array(img)
    else:
        raise ValueError("Unsupported file format")
