import os
import tkinter as tk
from tkinter import Label, Button, OptionMenu, StringVar, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from gui.load_image import load_image
import math
from tkinter import ttk
import tkinter.messagebox as messagebox


class MainWindow:
    def __init__(self, config):
        self.root = tk.Tk()
        self.root.title(config["window_title"])
        self.root.geometry(f"{config['default_window_size'][0]}x{config['default_window_size'][1]}")

        # Left frame for image display
        left_frame = ttk.Frame(self.root, padding=10)
        left_frame.pack(side="left", fill="both", expand=True)

        # Right frame for buttons and controls
        right_frame = ttk.Frame(self.root, width=200, padding=(10, 20))
        right_frame.pack(side="right", fill="y")

        # Load button
        load_button = ttk.Button(right_frame, text="Load Image", command=self.load_image)
        load_button.pack(pady=(0, 20), fill="x")

        # Image properties label
        self.image_info_label = ttk.Label(right_frame, text="Image properties will appear here", anchor="center")
        self.image_info_label.pack(pady=(0, 20), fill="x")

        # Colormap dropdown with label
        colormap_label = ttk.Label(right_frame, text="Select Colormap:")
        colormap_label.pack(anchor="w", pady=(0, 5))
        colormap_options = ["viridis", "gray", "plasma", "inferno", "magma", "jet"]
        self.colormap = tk.StringVar(value="viridis")
        colormap_menu = ttk.OptionMenu(right_frame, self.colormap, *colormap_options)
        colormap_menu.pack(fill="x", pady=(0, 20))

        # Channel dropdown with label
        channel_label = ttk.Label(right_frame, text="Select Channel:")
        channel_label.pack(anchor="w", pady=(0, 5))
        self.channel_options = ["All", "Channel 0", "Channel 1", "Channel 2"]
        self.channel = tk.StringVar(value="All")
        self.channel_menu = ttk.OptionMenu(right_frame, self.channel, *self.channel_options)
        self.channel_menu.pack(fill="x", pady=(0, 20))

        # Apply button for showing selected image settings
        show_button = ttk.Button(right_frame, text="Apply", command=self.show_image)
        show_button.pack(fill="x", pady=(0, 20))

        # Plot All Channels button
        plot_all_button = ttk.Button(right_frame, text="Plot All Channels", command=self.plot_all_channels)
        plot_all_button.pack(fill="x", pady=(0, 20))

        # Matplotlib figure and canvas setup
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=left_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Add toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, left_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.npy *.jpg *.png")])
        if filepath:
            self.img_array = load_image(filepath)
            self.update_image_info()
            # Enable channel selection only if it's a multi-channel image
            if self.img_array.ndim == 3:
                self.channel_options = [f"Channel {i}" for i in range(self.img_array.shape[2])]
                self.channel.set("All")
                self.channel_menu['menu'].delete(0, 'end')
                for option in self.channel_options:
                    self.channel_menu['menu'].add_command(label=option, command=tk._setit(self.channel, option))
                self.channel_menu.configure(state="normal")
            else:
                self.channel.set("All")
                self.channel_menu.configure(state="disabled")

    def update_image_info(self):
        if self.img_array is not None:
            dimensions = f"Dimensions: {self.img_array.shape}"
            dtype = f"Data Type: {self.img_array.dtype}"
            info_text = f"{dimensions}\n{dtype}"
            self.image_info_label.config(text=info_text)

    def show_image(self):
        if self.img_array is None:
            return

        # Get colormap and selected channel
        selected_colormap = self.colormap.get()
        selected_channel = self.channel.get()

        # Check for invalid channel dimensions
        if self.img_array.ndim == 3 and self.img_array.shape[2] not in [1, 3] and selected_channel == "All":
            print(self.img_array.shape)
            messagebox.showerror("Invalid Image Format", "The image should have either 1 or 3 channels.")
            return

        # Process the selected channel
        elif selected_channel != "All" and self.img_array.ndim == 3:
            channel_index = int(selected_channel.split()[-1])  # Get channel index
            img_to_display = self.img_array[:, :, channel_index]
        else:
            img_to_display = self.img_array

        # Clear the previous plot and display the new image
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.imshow(img_to_display, cmap=selected_colormap if img_to_display.ndim == 2 else None)
        self.canvas.draw()

    def plot_all_channels(self):
        if self.img_array is None or self.img_array.ndim != 3:
            return

        num_channels = self.img_array.shape[2]
        cols = math.ceil(num_channels**0.5)
        rows = math.ceil(num_channels / cols)

        # Clear the previous plot
        self.fig.clear()

        for i in range(num_channels):
            ax = self.fig.add_subplot(rows, cols, i + 1)
            ax.imshow(self.img_array[:, :, i], cmap=self.colormap.get())
            ax.set_title(f'Channel {i}')
            ax.axis('off')  # Hide axes

        self.canvas.draw()

    def run(self):
        self.root.mainloop()
