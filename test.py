from PIL import Image

# List of images
images_paths = ['test1999/2_0.jpg', 'test1999/2_1.jpg', 'test1999/2_2.jpg', 'test1999/2_3.jpg', 'test1999/2_4.jpg',
                'test1999/2_5.jpg', 'test1999/2_6.jpg', 'test1999/2_7.jpg', 'test1999/2_8.jpg', 'test1999/2_8.jpg']

# Open the input images
images_list = [Image.open(image) for image in images_paths]

# Determine the width and height of the stitched image
width = sum([image.width for image in images_list])
height = max([image.height for image in images_list])

# Create a new blank image with the calculated dimensions
stitched_image = Image.new('RGB', (width, height))

# Paste the individual images onto the stitched image
cummulative_width = 0
for image in images_list:
    stitched_image.paste(image, (cummulative_width, 0))
    cummulative_width += image.width

# Save the stitched image
stitched_image.save('test19.png')

# Close all images
for image in images_list:
    image.close()