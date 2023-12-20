import cv2
import os
import tkinter as tk
from tkinter import filedialog

class ImageClassifier:
    def __init__(self, root, image_paths):
        self.root = root
        self.image_paths = image_paths
        self.current_index = 0

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        self.load_image()

        # Buttons for navigation
        tk.Button(root, text="Previous", command=self.prev_image).pack(side=tk.LEFT)
        tk.Button(root, text="Next", command=self.next_image).pack(side=tk.RIGHT)

        # Button for reclassification
        tk.Button(root, text="Do something", command=self.do_something).pack()

    def load_image(self):
        image_path = self.image_paths[self.current_index]
        image = cv2.imread(image_path)
        image = cv2.resize(image,dsize=(0,0), fx=0.5, fy=0.5)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCV loads images in BGR, convert to RGB
        photo = ImageTk.PhotoImage(Image.fromarray(image))

        self.canvas.config(width=photo.width(), height=photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image()

    def next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.load_image()

    def do_something(self):
        # TODO: Add function
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Viewer")

    image_folder = filedialog.askdirectory(title="Select Image Folder")
    image_paths = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if image_paths:
        from PIL import Image, ImageTk
        app = ImageClassifier(root, image_paths)
        root.mainloop()
    else:
        print("No images found in the selected folder.")
