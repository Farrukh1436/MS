import os
from PIL import Image, ImageTk
def iconik(name,size):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, f"../images/{name}.png")
    
    # Load and resize the home button icon
    p_icon = Image.open(image_path)
    p_icon = p_icon.resize((size, size), Image.LANCZOS)  # Resize to 32x32 pixels
    icon = ImageTk.PhotoImage(p_icon)
    return icon
def l_im(image_files, scale_factor=1):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tk_images = []

    try:
        for image_file in image_files:
            image_path = os.path.join(script_dir, f"../images/{image_file}.png")
            pil_image = Image.open(image_path)

            # Scale the image
            original_width, original_height = pil_image.size
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
            pil_image = pil_image.convert("RGBA")

            tk_image = ImageTk.PhotoImage(pil_image)
            tk_images.append(tk_image)

    except (FileNotFoundError, IOError) as e:
        print(f"Error loading image: {e}")
        raise

    return tk_images