import matplotlib.pyplot as plt
from core.file_handler import validate_image

class Display:
    def show_image(self, img_array, colormap="viridis"):
        if not validate_image(img_array):
            raise ValueError("Invalid image format")
        
        plt.imshow(img_array, cmap=colormap if img_array.ndim == 2 else None)
        plt.colorbar()
        plt.show()
