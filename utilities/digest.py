import colorgram
from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean
from skimage import io
from skimage import img_as_ubyte
from PIL import Image
import os

def digest(root):
    color_sample=18
    row_multiplier=50
    col_multiplier=50
    seperator=[30,33,37]

    # find all image paths
    images_path=[]
    for i in os.listdir(root):
        if os.path.isdir(os.path.join(root,i)):
            images_path=images_path+[os.path.join(i,j) for j in os.listdir(os.path.join(root,i))]
        else:
            images_path.append(i)
    print(images_path)
    image_number=len(images_path)

    # extract dominant colors
    colors_raw = []
    while len(colors_raw)!=image_number:
        try:
            colors_raw=[]
            for i in images_path:
                image = io.imread(os.path.join(root, i))
                # downscale to 512*512
                x = image.shape[0]
                y = image.shape[1]
                while x*y > 512*512:
                    x = x//2
                    y = y//2
                    new_shape = (x, y, image.shape[2])
                image_rescaled = resize(image, new_shape, preserve_range=True)
                io.imsave('image.png', image_rescaled)
                dominant_colors = colorgram.extract('image.png', color_sample)
                assert len(dominant_colors) == color_sample
                colors_raw.append(dominant_colors)
        except AssertionError as e:
            print(f"Reduce color sample from {color_sample} to {len(dominant_colors)} ")
            color_sample = len(dominant_colors)



    colors_format=[]
    for dominant_colors in colors_raw:
        dominant_color_format=[]
        for i in dominant_colors:
            dominant_color_format=dominant_color_format+[i.rgb.r, i.rgb.g, i.rgb.b]*col_multiplier
        colors_format.extend(dominant_color_format*row_multiplier)
        if seperator!=[]:
            colors_format.extend(seperator*col_multiplier*color_sample*5)
    colors_byte = bytes(colors_format)

    print(color_sample)
    print(image_number)
    print(len(colors_format))
    print(len(colors_raw))
    print([len(i) for i in colors_raw])


    img = Image.frombytes('RGB', (color_sample*col_multiplier, image_number*row_multiplier), colors_byte)
    img.show()
    img.save(os.path.join(root,'digest.png'))

if __name__ == "__main__":
    digest('./')