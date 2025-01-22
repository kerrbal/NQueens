from PIL import Image
import numpy as np

#For masking the queen

img = Image.open(r"queen.png")

img = img.convert("RGBA")
pixels = np.array(img)
booleans = np.all(pixels[:, :, :3] < 220, axis = 2)
for i in range(len(booleans)):
    for j in range(len(booleans[0])):
        #black
        if booleans[i, j]:
            pixels[i, j, 3] = 255
        #white
        else:
            pixels[i, j, 3] = 0


new_img = Image.fromarray(pixels, mode = "RGBA")
new_img.save("masked_queen.png")