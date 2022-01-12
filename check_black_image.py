import cv2
import os
import sys
import cv2
import tqdm
import shutil
import numpy as np
import matplotlib.pyplot as plt
from utils.util import *

"""
  사용 목적:
    이미지에서 사람 객체가 일정 이상의 검은색을 띄고 있으면 이미지를 copy 하는 코드
  
  get_file_list 함수는 공개 x
"""

def cut_threshold(image, ROI_threshold, threshold):
    ROI_threshold = cv2.threshold(image, ROI_threshold, 255, cv2.THRESH_BINARY)  # 0 ~ 255   # first threshold
    unique, count = (np.unique(ROI_threshold[1], return_counts=True))
    uniq_count = dict(zip(unique, count))

    if 0 not in uniq_count.keys():  # 0이 없고 255인 경우 처리
        result = False
    else:
        result = ((uniq_count[0] / (uniq_count[0] + uniq_count[255])) * 100) > threshold

    return result

def main(ROI_threshold, threshold):
    copy_path = ''
    path = ''

    img_list = get_file_list(path, '.jpg')
    txt_list = get_file_list(path, '.txt')

    black_file_name_list = list()
    for img, txt in tqdm(zip(img_list, txt_list), total=len(img_list), desc='check black bounding box...'):
        if img.split('.jpg') == txt.split('.txt'):    # check file name is same
            txt_path = os.path.join(path, txt)
            img_path = os.path.join(path, img)

            image = cv2.imread(img_path, cv2.IMREAD_COLOR)
            with open(txt_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    bbox = line.strip().split()
                    bbox = list(map(int, bbox))  # 리스트 내 타입 변경
                    xmin, ymin, xmax, ymax = bbox[1:5]

                    ROI = image[ymin:ymax, xmin:xmax]                   # boundnig box
                    gray_ROI = cv2.cvtColor(ROI, cv2.COLOR_RGB2GRAY)    # convert to gray

                    if cut_threshold(gray_ROI, ROI_threshold=ROI_threshold, threshold=threshold):
                        black_file_name_list.append(img)
                        shutil.copy(os.path.join(path, img), os.path.join(copy_path, img))
                        continue    # 박스 한개라도 검은색이면 복사
                        
if __name__ == '__main__':
    ROI_threshold = 20      # pixel 값이 20 이하면 0으로 20 초과면 255로 바꿔준다.
    threshold = 85          # 전체 pixle 비중에서 0의 pixel이 threshold 이상인 경우
    main(ROI_threshold, threshold)
