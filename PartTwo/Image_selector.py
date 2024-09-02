import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import numpy as np
from Image_details import ImageDetailsPage

class ImageSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Select Image")
        self.root.geometry("600x500")
        root.resizable(False, False)

        self.selected_image_path = None
        self.details_window = None  

        self.initialize_ui()

    def initialize_ui(self):
        self.root.tk_setPalette(background='#e8e8e8')

        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background="#e8e8e8")

        self.main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.button_frame.pack(pady=5, anchor="w")

        self.file_button = ttk.Button(self.button_frame, text="Select Image", command=self.select_file, width=20)
        self.file_button.pack(side="left", padx=5)

        self.select_button = ttk.Button(self.button_frame, text="Next", command=self.show_details_window, width=20)
        self.select_button.pack(side="left", padx=5)

        self.blue_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.blue_frame.pack(pady=10, expand=True, fill=tk.BOTH)

        self.image_frame = ttk.Frame(self.blue_frame, style="Custom.TFrame", width=300, height=300)
        self.image_frame.pack(pady=10)

        self.gray_frame = tk.Frame(self.image_frame, bg="#e8e8e8", width=300, height=300)
        self.gray_frame.pack(expand=True)

        self.canvas = tk.Canvas(self.gray_frame, bg="#e8e8e8", width=300, height=300)
        self.canvas.pack(expand=True)

        self.no_image_label = ttk.Label(self.canvas, text="No image selected", font=("Helvetica", 14, "italic"), foreground="black", background="#e8e8e8")
        self.no_image_label.place(relx=0.5, rely=0.5, anchor="center")

        self.image_title_label = ttk.Label(self.blue_frame, text="", font=("Helvetica", 14, "bold"), background="#e8e8e8")
        self.image_title_label.pack(pady=(0, 10), padx=10, anchor="center")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
        if file_path:
            self.selected_image_path = file_path
            self.load_image()

    def load_image(self):
        try:
            image = Image.open(self.selected_image_path).convert('L')  # Convert to grayscale

            box_width, box_height = 300, 300

            original_width, original_height = image.size

            if original_width <= box_width and original_height <= box_height:
                preview_size = (original_width, original_height)
            else:
                preview_size = (box_width, box_height)
                image.thumbnail(preview_size, Image.LANCZOS)

            self.canvas.config(width=box_width, height=box_height)
            self.image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")  
            self.canvas.create_image(box_width // 2, box_height // 2, anchor="center", image=self.image)

            self.no_image_label.place_forget()

            self.image_title_label.config(text=os.path.basename(self.selected_image_path))
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image:\n{str(e)}")
            self.selected_image_path = None
            self.canvas.delete("all")
            self.no_image_label.place(relx=0.5, rely=0.5, anchor="center")  # Mostra l'etichetta "No image selected"
            self.image_title_label.config(text="")

    def show_details_window(self):
        if self.selected_image_path:
            if self.details_window and self.details_window.winfo_exists():
                self.details_window.destroy()

            self.details_window = tk.Toplevel(self.root)
            self.details_window.title("Image Details")
            self.details_window.geometry("450x500")
            self.details_window.resizable(False, False)
            self.details_window.protocol("WM_DELETE_WINDOW", self.close_details_window)
            
            details_page = ImageDetailsPage(self.details_window, self.selected_image_path)
            details_page.pack(fill="both", expand=True)
        else:
            messagebox.showwarning("No Image", "Select an image before proceeding")

    def close_details_window(self):
        self.details_window.destroy()
        self.details_window = None