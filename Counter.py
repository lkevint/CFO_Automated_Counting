import cv2
import scipy
from scipy import signal
import numpy as np
import math
import copy
import gc

class Counter:
    def __init__(self, video, start_time, damage_x, damage_y, stuns_x, stuns_y, height, width, brightness, bonus):
        self.score = []
        global damages
        damages = [0]
        global stuns
        stuns = []
        global crnn
        crnn = self.loadCRNN()

        cap = cv2.VideoCapture(video)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        comparison_damage = np.zeros((height, width), dtype=np.uint8)
        comparison_stuns = np.zeros((height, width), dtype=np.uint8)
        count = 0

        for i in range(int(start_time * self.fps)):
            cap.grab()

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                #converts image into grayscale, then into binary for processing
                binary_damage = cv2.threshold(cv2.cvtColor(frame[damage_y:damage_y + height, damage_x:damage_x + width], cv2.COLOR_BGR2GRAY),\
                brightness, 255, cv2.THRESH_BINARY)[1]
                binary_stuns = cv2.threshold(cv2.cvtColor(frame[stuns_y:stuns_y + height, stuns_x:stuns_x + width], cv2.COLOR_BGR2GRAY),\
                brightness, 255, cv2.THRESH_BINARY)[1]
                damages.append(self.readDamage(binary_damage, comparison_damage))
                comparison_damage = binary_damage.copy()
                if self.processStuns(binary_stuns, comparison_stuns):
                    stuns.append(count)
                comparison_stuns = binary_stuns.copy()
                count += 1
            else:
                break

        cap.release()
        damages = damages[1:]
        damages = self.processDamages(damages)
        self.score = self.processScore(damages, stuns, bonus)

    #load CRNN model
    def loadCRNN(self):
        crnn = cv2.dnn.TextRecognitionModel('resources/crnn.onnx')
        crnn.setDecodeType("CTC-greedy")
        alphabet = '0123456789'
        crnn.setVocabulary(alphabet)
        crnn.setInputParams(1/127.5, [100, 32], [127.5, 127.5, 127.5])
        return crnn

    #reads damage from input image if differs from comparison
    def readDamage(self, image, comparison):
        if np.sum(cv2.absdiff(image, comparison)) == 0:
            return damages[-1]
        damage_result = crnn.recognize(image)
        if damage_result == '':
            return 0
        else:
            return int(damage_result)

    def processDamages(self, damage_list):
        damage_list = list(scipy.signal.medfilt(damage_list, 7))
        final_damage = [damage_list.pop()]
        for elem in np.flip(damage_list):
            if final_damage[-1] == 0:
                final_damage.append(0)
            elif elem > 11 * final_damage[-1]:
                final_damage.append(math.floor(elem/100))
            elif elem - final_damage[-1] > 100:
                final_damage.append(math.floor(elem/10))
            else:
                final_damage.append(elem)

        final_damage.reverse()
        damage_times = [[0, 0]]
        for i in range(len(final_damage)):
            if final_damage[i] != damage_times[-1][0]:
                damage_times.append([final_damage[i], i])
        return damage_times

    def processStuns(self, image, comparison):
        diff = np.sum(cv2.absdiff(image, comparison))
        if  diff > 20000:
            return True
        return False

    def processScore(self, damage_list, stun_list, bonus):
        score_times = copy.deepcopy(damage_list)
        modifier = 0

        for elem in score_times:
            if elem[1] in stun_list:
                modifier += 10
            elem[0] = elem[0] + modifier

        if not bonus:
            for elem in score_times:
                elem[1] = int(30 * elem[1]/self.fps)
            return score_times

        for elem in bonus:
            elem[1] = int(elem[1] * self.fps)
            insert = True

            for i in range(len(score_times)):
                if elem[1] == score_times[i][1]:
                    insert = False
                    score_times[i][0] += elem[0]
                if elem[1] < score_times[i][1]:
                    score_times[i][0] += elem[0]

            if insert:
                if elem[1] < score_times[1][1]:
                    score_times.insert(1, elem)
                else:
                    counter = 0
                    for i in range(len(score_times) - 1):
                        i = i + counter
                        if i == len(score_times) - 2:
                            score_times.append([elem[0] + score_times[-1][0], elem[1]])
                            break
                        elif elem[1] < score_times[i + 1][1] and elem[1] > score_times[i][1]:
                            score_times.insert(i + 1, [elem[0] + score_times[i][0], elem[1]])
                            counter += 1
                            break

        for elem in score_times:
            elem[1] = int(30 * elem[1]/self.fps)

        return score_times
