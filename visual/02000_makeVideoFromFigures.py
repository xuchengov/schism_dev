### If package not imported, make sure to install the packages below
###  pip install imageio[ffmpeg] opencv-python
import cv2
import glob

# Get image files sorted by name
image_files = sorted(glob.glob("Figure_*.png"))  # Sorts Fig1.png, Fig2.png, etc.

# Read the first image to get dimensions
frame = cv2.imread(image_files[0])
height, width, layers = frame.shape

# Define the video codec and create VideoWriter object
video = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

# Add images to the video
for image in image_files:
    img = cv2.imread(image)
    video.write(img)

# Release the video writer
video.release()
print("Video saved as output.mp4")




