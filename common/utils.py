from PIL import Image

# utility functions


def resize_image(path, x, y):
    img = Image.open(path)

    if img.height > x or img.width > y:
        output_size = (x, y)
        img.thumbnail(output_size)
            
        img.save(path)

def ComputeProminentColor(path):
    print(path)
    img = Image.open(path)

    colors = img.convert('RGBA').getcolors(img.size[0]*img.size[1])

    # select only colors above a certain level of transparency
    filtered_colors = list(filter(lambda x : x[1][3] > 155, colors))
    
    prominent_hex = '000000'    # hex black

   

    if len(filtered_colors) != 0:
        sorted_colors = list(sorted(filtered_colors, key=lambda x: x[0], reverse=True))
        p = sorted_colors[0]
        if p[1][3] == 255:
            prominent_hex = '%02x%02x%02x' % (round(p[1][0]), round(p[1][1]), round(p[1][2]))
        else:
            prominent_hex = '%02x%02x%02x%02x' % (round(p[1][0]), round(p[1][1]), round(p[1][2]), round(p[1][3]))

    return prominent_hex

def CreateBannerFromColors(path):
    pass