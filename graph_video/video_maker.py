import cv2

SAVE_DIR = "video"

fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter(f"{SAVE_DIR}/video_60fps_10000throws.avi", fourcc, 60.0, (1200, 700))


for i in range(10000):
    img_path = f"images/{i}.png"
    print(img_path)
    frame = cv2.imread(img_path)
    out.write(frame)

out.release()