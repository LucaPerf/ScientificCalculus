import numpy as np
from scipy.fft import dct, idct
from PIL import Image
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox

def flow(image_path, F, d):
    print(f"Processing image: {image_path}")
    print(f"F: {F}, d: {d}")

    blocks, image_original = divide_image(image_path, F)
    dct2_blocks = apply_dct2(blocks, d)

    for i, dct2_block in enumerate(dct2_blocks[:3]):
        print(f"Results of DCT2 by block {i+1}: \n {dct2_block}\n")

    idct2_blocks = apply_idct2(dct2_blocks)
    reconstructed_image = reconstruct_image(idct2_blocks, F, image_path)
    visualize_images(image_original, reconstructed_image)

# calculation of DCT2 with library
def dct2_library(matrix):
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')

# calculation of IDCT2 with library
def idct2_library(coefficients):
    return idct(idct(coefficients.T, norm='ortho').T, norm='ortho')

# check the input variables
def check_variables(F, d, image_path, parent_window):
    if not F and not d:
        messagebox.showerror("Error", "Enter the values of F and d.", parent=parent_window)
        return

    if not F:
        messagebox.showerror("Error", "Enter the value of F", parent=parent_window)
        return

    if not d:
        messagebox.showerror("Error", "Enter the value of d.", parent=parent_window)
        return

    if not is_integer(F):
        messagebox.showerror("Error", "F must be an integer.", parent=parent_window)
        return

    if not is_integer(d):
        messagebox.showerror("Error", "d must be an integer.", parent=parent_window)
        return

    F = int(F)
    d = int(d)

    if F < 0:
        messagebox.showerror("Error", "F must be greater than or equal to 0.", parent=parent_window)
        return
    if d < 0:
        messagebox.showerror("Error", "d must be greater than or equal to 0.", parent=parent_window)
        return

    # Check that the value of F is not greater than the height/width of the image
    try:
        with Image.open(image_path) as img:
            img_width, img_height = img.size

        if F > img_width or F > img_height:
            messagebox.showerror("Error", "The value of F cannot exceed the size of the image.", parent=parent_window)
            return
        
        print("Image Width:", img_width)
        print("Image Height:", img_height)

    except Exception as e:
        messagebox.showerror("Error", f"Error when retrieving image size: {str(e)}", parent=parent_window)
        return

    # Checks that the value of 'd' is between 0 and 2F-2
    if d > 2 * F - 2 or d < 0:
        messagebox.showerror("Error", "The value of d should be between 0 and 2F-2.", parent=parent_window)
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
        print('open')
    except IOError:
        print(f"Unable to open image {image_path}.")
        return [], None
            
    print('Open image')
    
    img_width, img_height = image.size
    print(f'Image size: width={img_width}, height={img_height}')

    # Convert image to grayscale
    img_gray = image.convert('L')

    # Calculating the number of blocks horizontally and vertically
    num_blocks_horizontal = img_width // F
    num_blocks_vertical = img_height // F
    print(f'Number of blocks: horizontal={num_blocks_horizontal}, verticals={num_blocks_vertical}')

    blocks = []

    for j in range(num_blocks_vertical):
        for i in range(num_blocks_horizontal):
            # Calculation of start and end coordinates of the current block
            x0 = i * F
            y0 = j * F
            x1 = x0 + F
            y1 = y0 + F
            print(f'Block {len(blocks)+1}: ({x0}, {y0}, {x1}, {y1})')

            block = img_gray.crop((x0, y0, x1, y1))
            blocks.append(block)
    
    print(f'Divided {len(blocks)} size blocks {F}x{F}')
    return blocks, img_gray

# Apply DCT2
def apply_dct2(blocks, cut):
    dct2_blocks = []
    for block in blocks:
        block_array = np.array(block)
        dct2_block = dct2_library(block_array)
        for i in range(dct2_block.shape[0]):
            for j in range(dct2_block.shape[1]):
                if i + j >= cut:
                    dct2_block[i, j] = 0 
        dct2_blocks.append(dct2_block)
    print(f"Applied DCT2 to {len(dct2_blocks)} blocks")
    return dct2_blocks

# Apply IDCT2
def apply_idct2(dct2_blocks):
    idct2_blocks_rounded = []
    for block in dct2_blocks:
        idct2_block = idct2_library(block)
        idct2_block_rounded = np.round(idct2_block)
        idct2_block_rounded[idct2_block_rounded < 0] = 0
        idct2_block_rounded[idct2_block_rounded > 255] = 255
        idct2_block_rounded = idct2_block_rounded.astype(np.uint8)
        idct2_blocks_rounded.append(idct2_block_rounded)
    print(f"Applied IDCT2 to {len(idct2_blocks_rounded)} blocks")
    return idct2_blocks_rounded

# Recompose the compressed image using compressed blocks.
def reconstruct_image(blocks_idct_rounded, F, image_path):
    try:
        img_width, img_height = Image.open(image_path).size
        compressed_image = Image.new('L', (img_width, img_height))

        num_blocks_horizontal = img_width // int(F)

        for j in range(img_height // int(F)):
            for i in range(num_blocks_horizontal):
                x0 = i * int(F)
                y0 = j * int(F)

                if not blocks_idct_rounded:
                    raise ValueError("Empty IDCT block list before image reconstruction")

                block = blocks_idct_rounded.pop(0)

                compressed_image.paste(Image.fromarray(block), (x0, y0))

        return compressed_image

    except Exception as e:
        print("Error during image reconstruction:", str(e))
        return None  # Restituisce None in caso di errore

def visualize_images(original_image, reconstructed_image):
    if original_image is None or reconstructed_image is None:
        print("Unable to view images.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # View original image
    axes[0].imshow(original_image, cmap='gray')
    axes[0].set_title('Original image')

    # Convert the reconstructed image to a array
    reconstructed_image_array = np.array(reconstructed_image)

    # View the reconstructed image
    axes[1].imshow(reconstructed_image_array, cmap='gray')
    axes[1].set_title('Reconstructed image')

    plt.tight_layout()
    plt.show()
