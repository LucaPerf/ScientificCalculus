import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import PartTwo.utils_part2 as utils_part2  # Assicurati che sia importato correttamente

class ImageDetailsPage(ttk.Frame):
    def __init__(self, parent, selected_image_path=None):
        super().__init__(parent)
        self.parent = parent
        self.image_path = selected_image_path or ""

        # Creazione del Canvas all'interno del Frame principale
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Creazione dello Scrollbar verticale
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Binding della scrollbar al canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Creazione del Frame interno al Canvas
        self.inner_frame = ttk.Frame(self.canvas)
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Binding per lo scrolling con la rotellina del mouse
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.initialize_ui()

        # Carica i dettagli dell'immagine se è stato fornito un percorso
        if self.image_path:
            self.load_image_details()

    def on_scroll(self, *args):
        self.canvas.yview(*args)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def initialize_ui(self):
        # Titolo dell'immagine
        self.title_label = ttk.Label(self.inner_frame, text="", font=("Helvetica", 14, "bold"))
        self.title_label.pack(side="top", pady=10)

        # Frame per visualizzare l'immagine
        self.image_frame = ttk.Frame(self.inner_frame, width=300, height=300)
        self.image_frame.pack(pady=10)

        # Percorso dell'immagine
        self.path_label = ttk.Label(self.inner_frame, text="Percorso:", font=("Helvetica", 10, "bold"))
        self.path_label.pack(anchor="w", padx=5, pady=(10, 5))

        self.path_value = ttk.Label(self.inner_frame, text="", wraplength=400)
        self.path_value.pack(anchor="w", padx=5)

        # Dimensioni dell'immagine originale
        self.size_label = ttk.Label(self.inner_frame, text="Dimensione originale:", font=("Helvetica", 10, "bold"))
        self.size_label.pack(anchor="w", padx=5, pady=(10, 5))

        self.size_value = ttk.Label(self.inner_frame, text="")
        self.size_value.pack(anchor="w", padx=5)

        # Frame per i campi di input
        input_frame = ttk.Frame(self.inner_frame)
        input_frame.pack(pady=10)

        # Etichette e campi di input per dimensione finestrella e soglia di taglio
        size_label = ttk.Label(input_frame, text="Dimensione Finestrella:", font=("Helvetica", 10, "bold"))
        size_label.pack(pady=5)
        self.size_entry = ttk.Entry(input_frame)
        self.size_entry.pack(pady=5)

        threshold_label = ttk.Label(input_frame, text="Soglia di Taglio:", font=("Helvetica", 10, "bold"))
        threshold_label.pack(pady=5)
        self.threshold_entry = ttk.Entry(input_frame)
        self.threshold_entry.pack(pady=5)

        # Bottone di avvio
        start_button = ttk.Button(input_frame, text="Avvio", command=self.start_processing)
        start_button.pack(pady=10)

        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def load_image_details(self):
        self.title_label.config(text=os.path.basename(self.image_path))
        self.path_value.config(text=self.image_path)
        self.load_image()
        original_size = self.get_image_size()
        self.size_value.config(text=f"{original_size[0]} x {original_size[1]}")

    def get_image_size(self):
        try:
            with Image.open(self.image_path) as img:
                return img.size
        except Exception as e:
            print(f"Errore nel ottenere la dimensione dell'immagine {self.image_path}: {e}")
            return (0, 0)

    def load_image(self):
        try:
            image = Image.open(self.image_path)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)
            img_label = ttk.Label(self.image_frame, image=photo)
            img_label.photo = photo
            img_label.pack(expand=True)
        except Exception as e:
            print(f"Errore nel caricamento dell'immagine {self.image_path}: {e}")

    def start_processing(self):
        F = self.size_entry.get()
        d = self.threshold_entry.get()

        if not utils_part2.check_variables(F, d, self.image_path, self):
            return    
        
        F = int(self.size_entry.get())
        d = int(self.threshold_entry.get())
        print(f"Dimensione Finestrella: {F}, Soglia di Taglio: {d}")

        self.process_image(F, d)
    
    def process_image(self, F, d):
        utils_part2.flow(self.image_path, F, d)  # Passa i parametri alla funzione flow
    
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.inner_frame_id, width=self.canvas.winfo_width())
