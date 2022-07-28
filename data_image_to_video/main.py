import cv2
import os

image_folder = 'D:/Works/STUDY/PJ_IOT/fp_artificialIntelligence/serial_mlx90640_scraping/data/MLX90640_TWO-PERSON_WALLVIEW/images'
video_name = 'video.mp4'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 6, (width,height))

for image in images:
    print(image)
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()