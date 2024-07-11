import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import numpy as np
from Image_details import ImageDetailsPage

class ImageSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Selezione Immagine")
        self.root.geometry("600x500")
        root.resizable(False, False)

        self.selected_image_path = None
        self.details_window = None  # Finestra per i dettagli dell'immagine

        self.initialize_ui()

    def initialize_ui(self):
        # Impostazione del colore di sfondo della finestra principale
        self.root.tk_setPalette(background='#e8e8e8')

        # Stile personalizzato per tutti i frame e canvas
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background="#e8e8e8")

        # Frame principale
        self.main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Frame per i pulsanti
        self.button_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.button_frame.pack(pady=5, anchor="w")

        # Pulsante per selezionare l'immagine
        self.file_button = ttk.Button(self.button_frame, text="Seleziona Immagine", command=self.select_file)
        self.file_button.pack(side="left", padx=5)

        # Pulsante per mostrare i dettagli dell'immagine
        self.select_button = ttk.Button(self.button_frame, text="Continua", command=self.show_details_window)
        self.select_button.pack(side="left", padx=5)

        # Frame grgio esterno
        self.blue_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.blue_frame.pack(pady=10, expand=True, fill=tk.BOTH)

        # Frame per mostrare l'immagine selezionata con padding
        self.image_frame = ttk.Frame(self.blue_frame, style="Custom.TFrame", width=300, height=300)
        self.image_frame.pack(pady=10)

        # Creazione del riquadro grigio
        self.gray_frame = tk.Frame(self.image_frame, bg="#e8e8e8", width=300, height=300)
        self.gray_frame.pack(expand=True)

        # Canvas per mostrare l'immagine al centro
        self.canvas = tk.Canvas(self.gray_frame, bg="#e8e8e8", width=300, height=300)
        self.canvas.pack(expand=True)

        # Etichetta "No image selected"
        self.no_image_label = ttk.Label(self.canvas, text="No image selected", font=("Helvetica", 14, "italic"), foreground="black", background="#e8e8e8")
        self.no_image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Etichetta per il titolo dell'immagine
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

            # Calcola le dimensioni del riquadro
            box_width, box_height = 300, 300

            # Dimensioni originali dell'immagine
            original_width, original_height = image.size

            # Mantieni le dimensioni originali se l'immagine è più piccola del riquadro
            if original_width <= box_width and original_height <= box_height:
                preview_size = (original_width, original_height)
            else:
                # Ridimensiona l'immagine per l'anteprima se necessario
                preview_size = (box_width, box_height)
                image.thumbnail(preview_size, Image.LANCZOS)

            # Centra l'immagine nel canvas
            self.canvas.config(width=box_width, height=box_height)
            self.image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")  # Cancella eventuali immagini precedenti sul Canvas
            self.canvas.create_image(box_width // 2, box_height // 2, anchor="center", image=self.image)

            # Nascondi l'etichetta "No image selected"
            self.no_image_label.place_forget()

            # Aggiorna il titolo dell'immagine
            self.image_title_label.config(text=os.path.basename(self.selected_image_path))
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel caricamento dell'immagine:\n{str(e)}")
            self.selected_image_path = None
            self.canvas.delete("all")
            self.no_image_label.place(relx=0.5, rely=0.5, anchor="center")  # Mostra l'etichetta "No image selected"
            self.image_title_label.config(text="")

    def show_details_window(self):
        if self.selected_image_path:
            if self.details_window and self.details_window.winfo_exists():
                self.details_window.destroy()

            self.details_window = tk.Toplevel(self.root)
            self.details_window.title("Dettagli Immagine")
            self.details_window.geometry("450x500")
            self.details_window.resizable(False, False)
            self.details_window.protocol("WM_DELETE_WINDOW", self.close_details_window)
            
            details_page = ImageDetailsPage(self.details_window, self.selected_image_path)
            details_page.pack(fill="both", expand=True)
        else:
            messagebox.showwarning("Nessuna Immagine", "Seleziona un'immagine prima di procedere.")

    def close_details_window(self):
        self.details_window.destroy()
        self.details_window = None