# -*- coding: utf-8 -*-
"""
@Author : Horizon
@Date   : 2021-03-28 15:54:32
"""

import os
import cv2
import json
import random
import argparse
import matplotlib.pyplot as plt

def get_msvd_item(msvd_path, anno):

    question = anno['question']
    answer = anno['answer']

    video_id = anno['video_id']

    cap = cv2.VideoCapture(os.path.join(msvd_path, "video/vid{}.avi".format(video_id)))

    assert cap.isOpened()

    _, first_frame = cap.read()

    first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)

    cap.release()

    return first_frame, question, answer



if(__name__ == "__main__"):

    parser = argparse.ArgumentParser(description='check data')
    parser.add_argument('--path', dest='path', default="F:/Dataset/MSVD-QA", type=str)
    args = parser.parse_args()

    msvd_path = args.path

    msvd_val_annotation_path = os.path.join(msvd_path, "val_qa.json")

    with open(msvd_val_annotation_path) as f:
        annotation = json.load(f)
    
    annotation_length = len(annotation)

    font={  'size': 15,
            'family': 'Times New Roman',
            'style':'italic'}

    plt.figure(1, figsize=(16, 9))
    plt.title("MSVD-QA dataset visualization")
    
    for i in range(4):

        random_index = random.randint(0, annotation_length)

        random_anno = annotation[random_index]

        frame, question, answer = get_msvd_item(msvd_path, random_anno)

        plt.subplot(2, 2, i+1, xticks=[], yticks=[])

        frame_height = frame.shape[0]

        plt.imshow(frame)
        plt.text(0, frame_height * 1.06, "Q: "+question.capitalize(), fontdict=font)
        plt.text(0, frame_height * 1.12, "A: "+answer.capitalize()  , fontdict=font)
    
    plt.show()

