import numpy as np
from scipy.fft import dct, idct
from PIL import Image
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox

def flow(image_path, F, d):
    # Esecuzione del codice
    print(f"Processing image: {image_path}")
    print(f"F: {F}, d: {d}")

    blocks, image_original = divide_image(image_path, F)
    dct2_blocks = apply_dct2(blocks, d)

    for i, dct2_block in enumerate(dct2_blocks[:3]):
        print(f"Resultati della DCT2 per blocco {i+1}: \n {dct2_block}\n")

    idct2_blocks = apply_idct2(dct2_blocks)
    reconstructed_image = reconstruct_image(idct2_blocks, F, image_path)
    visualize_images(image_original, reconstructed_image)

def dct2_library(matrix):
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')

def idct2_library(coefficients):
    return idct(idct(coefficients.T, norm='ortho').T, norm='ortho')

def check_variables(F, d, image_path, parent_window):
    if not F and not d:
        messagebox.showerror("Errore", "Inserisci i valori di F e d.", parent=parent_window)
        return

    if not F:
        messagebox.showerror("Errore", "Inserisci il valore di F.", parent=parent_window)
        return

    if not d:
        messagebox.showerror("Errore", "Inserisci il valore di d.", parent=parent_window)
        return

    if not is_integer(F):
        messagebox.showerror("Errore", "F deve essere un numero intero", parent=parent_window)
        return

    if not is_integer(d):
        messagebox.showerror("Errore", "d deve essere un numero intero", parent=parent_window)
        return

    F = int(F)
    d = int(d)

    if F < 0:
        messagebox.showerror("Errore", "F deve essere maggiore o uguale a 0", parent=parent_window)
        return
    if d < 0:
        messagebox.showerror("Errore", "d deve essere maggiore o uguale a 0", parent=parent_window)
        return

    # Verifichiamo ora che il valore di F non sia superiore all'altezza/larghezza dell'immagine
    try:
        with Image.open(image_path) as img:
            img_width, img_height = img.size

        if F > img_width or F > img_height:
            messagebox.showerror("Errore", "Il valore di F non può superare le dimensioni dell'immagine.", parent=parent_window)
            return

        # Stampa debug delle dimensioni dell'immagine selezionata
        print("Image Width:", img_width)
        print("Image Height:", img_height)

    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il recupero delle dimensioni dell'immagine: {str(e)}", parent=parent_window)
        return

    # verifichiamo che il valore di d sia compreso tra 0 e 2F-2
    if d > 2 * F - 2 or d < 0:
        messagebox.showerror("Errore", "Il valore di d deve essere compreso tra 0 e 2F-2.", parent=parent_window)
        return

    # If all checks pass, proceed with compression
    print("All test are ok.")
    return True

def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def divide_image(image_path, F):
    try:
        image = Image.open(image_path)
        print('aperta')
    except IOError:
        print(f"Impossibile aprire l'immagine {image_path}.")
        return [], None
            
    print('Immagine aperta')
    
    img_width, img_height = image.size
    print(f'Dimensioni immagine: larghezza={img_width}, altezza={img_height}')

    # Converti l'immagine in scala di grigi
    img_gray = image.convert('L')

    # Calcoliamo il numero di blocchi in orizzontale e verticale
    num_blocks_horizontal = img_width // F
    num_blocks_vertical = img_height // F
    print(f'Numero di blocchi: orizzontali={num_blocks_horizontal}, verticali={num_blocks_vertical}')

    blocks = []

    # Iteriamo su tutti i blocchi
    for j in range(num_blocks_vertical):
        for i in range(num_blocks_horizontal):
            # Calcoliamo le coordinate iniziali e finali del blocco corrente
            x0 = i * F
            y0 = j * F
            x1 = x0 + F
            y1 = y0 + F
            print(f'Blocco {len(blocks)+1}: ({x0}, {y0}, {x1}, {y1})')

            # Estraiamo il blocco corrente dall'immagine
            block = img_gray.crop((x0, y0, x1, y1))
            blocks.append(block)
    
    print(f'Divisi {len(blocks)} blocchi di dimensione {F}x{F}')
    return blocks, img_gray

def apply_dct2(blocks, cut):
    dct2_blocks = []
    for block in blocks:
        block_array = np.array(block)
        dct2_block = dct2_library(block_array)
        for i in range(dct2_block.shape[0]):
            for j in range(dct2_block.shape[1]):
                if i + j >= cut:
                    dct2_block[i, j] = 0  # Imposta a zero i coefficienti oltre la diagonale d
        dct2_blocks.append(dct2_block)
    print(f"Applicata DCT2 a {len(dct2_blocks)} blocchi")
    return dct2_blocks

def apply_idct2(dct2_blocks):
    idct2_blocks_rounded = []
    for block in dct2_blocks:
        idct2_block = idct2_library(block)
        idct2_block_rounded = np.round(idct2_block)
        idct2_block_rounded[idct2_block_rounded < 0] = 0
        idct2_block_rounded[idct2_block_rounded > 255] = 255
        idct2_block_rounded = idct2_block_rounded.astype(np.uint8)
        idct2_blocks_rounded.append(idct2_block_rounded)
    print(f"Applicata IDCT2 a {len(idct2_blocks_rounded)} blocchi")
    return idct2_blocks_rounded

def reconstruct_image(blocks_idct_rounded, F, image_path):
    try:
        # Ricomponi l'immagine compressa utilizzando i blocchi compressi
        img_width, img_height = Image.open(image_path).size
        compressed_image = Image.new('L', (img_width, img_height))

        num_blocks_horizontal = img_width // int(F)

        for j in range(img_height // int(F)):
            for i in range(num_blocks_horizontal):
                x0 = i * int(F)
                y0 = j * int(F)

                if not blocks_idct_rounded:
                    raise ValueError("Lista di blocchi IDCT vuota prima della ricostruzione dell'immagine")

                block = blocks_idct_rounded.pop(0)

                compressed_image.paste(Image.fromarray(block), (x0, y0))

        # Ritorna l'immagine compressa per la visualizzazione
        return compressed_image

    except Exception as e:
        print("Errore durante la ricostruzione dell'immagine:", str(e))
        return None  # Restituisce None in caso di errore

def visualize_images(original_image, reconstructed_image):
    if original_image is None or reconstructed_image is None:
        print("Impossibile visualizzare le immagini.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Visualizza l'immagine originale
    axes[0].imshow(original_image, cmap='gray')
    axes[0].set_title('Immagine originale')

    # Converti l'immagine ricostruita in un array numpy
    reconstructed_image_array = np.array(reconstructed_image)

    # Visualizza l'immagine ricostruita
    axes[1].imshow(reconstructed_image_array, cmap='gray')
    axes[1].set_title('Immagine ricostruita')

    plt.tight_layout()
    plt.show()
