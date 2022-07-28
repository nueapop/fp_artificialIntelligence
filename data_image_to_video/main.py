import cv2
import glob

frameSize = (500, 500)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('output_video.mp4',fourcc, 60, frameSize)

for filename in glob.glob('D:/Works/STUDY/PJ_IOT/fp_artificialIntelligence/serial_mlx90640_scraping/data/MLX90640_ONE-PERSON_WALLVIEW/images/*.png'):
    img = cv2.imread(filename)
    out.write(img)

out.release()