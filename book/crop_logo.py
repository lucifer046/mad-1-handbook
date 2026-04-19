from PIL import Image, ImageDraw, ImageOps

def crop_to_circle_with_background(image_path, output_path):
    # Open the image
    img = Image.open(image_path).convert("RGBA")
    
    # Create a background image with the theme color (Dark Slate)
    # Using the color (19, 27, 30) found in the logo's edge
    bg_color = (19, 27, 30, 255)
    final_img = Image.new('RGBA', img.size, bg_color)
    
    # Create a mask for the circle
    size = img.size
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    
    # Apply the mask to the original image
    img.putalpha(mask)
    
    # Paste the circular logo onto the solid background
    final_img.paste(img, (0, 0), img)
    
    # Save as PNG (solid background ensures no white corners on social platforms)
    final_img.save(output_path, "PNG")

if __name__ == "__main__":
    # We use a backup if logo.png is already cropped
    # but since we are overwriting, we just run it
    crop_to_circle_with_background("book/logo.png", "book/logo.png")
