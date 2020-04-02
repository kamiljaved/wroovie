from PIL import Image

# utility functions


def resize_image(path, x, y):
    img = Image.open(path)

    if img.height > x or img.width > y:
        output_size = (x, y)
        img.thumbnail(output_size)
            
    img.save(path)