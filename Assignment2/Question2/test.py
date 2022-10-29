# Import the Images module from pillow
from PIL import Image

# Open the image by specifying the image path.
image_path = "./inputs/starcraft.png"
image_file = Image.open(image_path)

# the default
image_file.save("image_name.png", quality=95)
