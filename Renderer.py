import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

class Renderer:
    def __init__(self, video, left, right):
        cap = cv2.VideoCapture(video)
        out = cv2.VideoWriter('rendered.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 30, (1920, 1080))
        left_info = [0, 1, left[1][1]]
        right_info = [0, 1, right[1][1]]
        count = 0

        while cap.isOpened():
            text = ""
            ret, frame = cap.read()
            if ret:
                if (count >= left_info[2]) and (left_info[1] < len(left) - 1):
                    left_info[0] = left[left_info[1]][0]
                    left_info[1] += 1
                    left_info[2] = left[left_info[1]][1]
                elif (count >= left_info[2]):
                    left_info[0] = left[left_info[1]][0]
                if (count >= right_info[2]) and (right_info[1] < len(right) - 1):
                    right_info[0] = right[right_info[1]][0]
                    right_info[1] += 1
                    right_info[2] = right[right_info[1]][1]
                elif (count >= right_info[2]):
                    right_info[0] = right[right_info[1]][0]

                text = str(left_info[0]) + ' - ' + str(right_info[0])

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                fontpath = 'akira_expanded.otf'
                font = ImageFont.truetype(fontpath, 70)
                pil_image = Image.fromarray(frame)
                draw_txt = ImageDraw.Draw(pil_image)
                width = draw_txt.textlength(text, font=font)
                textX = (frame.shape[1] - width) / 2
                draw_txt.text((textX, 120), text, font=font)
                frame = np.asarray(pil_image)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame)

                count += 1
            else:
                break

        cap.release()
        out.release()
