import numpy as np

def validate_image(array):
    if isinstance(array, np.ndarray) and array.ndim in [2, 3]:
        return True
    return False
