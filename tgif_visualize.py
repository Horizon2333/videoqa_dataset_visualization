# -*- coding: utf-8 -*-
"""
@Author : Horizon
@Date   : 2021-03-30 10:19:57
"""

import os
import numpy as np
import random
import argparse
from PIL import Image
import matplotlib.pyplot as plt

def get_tgif_item(tgif_path, anno, anno_type):

    first_frame = Image.open(os.path.join(tgif_path, os.path.join("gifs", anno[0]+".gif")))

    if(anno_type == "action" or anno_type == "transition"):

        question = anno[1]
        multi_choice = anno[2:7]
        answer = multi_choice[int(anno[7])]
    
    elif(anno_type == "count" or anno_type == "frameqa"):

        question = anno[1]
        multi_choice = []
        answer = anno[2]

    return first_frame, question, multi_choice, answer



if(__name__ == "__main__"):

    parser = argparse.ArgumentParser(description='check data')
    parser.add_argument('--path', dest='path', default="F:/Dataset/tgif-qa", type=str)
    args = parser.parse_args()

    tgif_path = args.path

    tgif_test_action_annotation_path     = os.path.join(tgif_path, "Test_action_question.csv"    )
    tgif_test_count_annotation_path      = os.path.join(tgif_path, "Test_count_question.csv"     )
    tgif_test_frameqa_annotation_path    = os.path.join(tgif_path, "Test_frameqa_question.csv"   )
    tgif_test_transition_annotation_path = os.path.join(tgif_path, "Test_transition_question.csv")
    
    tgif_test_action_annotation     = np.loadtxt(tgif_test_action_annotation_path    , dtype=str, delimiter='\t')
    tgif_test_count_annotation      = np.loadtxt(tgif_test_count_annotation_path     , dtype=str, delimiter='\t')
    tgif_test_frameqa_annotation    = np.loadtxt(tgif_test_frameqa_annotation_path   , dtype=str, delimiter='\t')
    tgif_test_transition_annotation = np.loadtxt(tgif_test_transition_annotation_path, dtype=str, delimiter='\t')

    tgif_test_annotation = [tgif_test_action_annotation, tgif_test_count_annotation, tgif_test_frameqa_annotation, tgif_test_transition_annotation]
    anno_types = ["action", "count", "frameqa", "transition"]

    font={  'size': 15,
            'family': 'Times New Roman',
            'style':'italic'}

    plt.figure(1, figsize=(16, 9))
    plt.title("tgif-qa dataset visualization")

    for i in range(4):

        annotation_length = len(tgif_test_annotation[i])

        random_index = random.randint(0, annotation_length)

        anno = tgif_test_annotation[i][random_index]

        gif_path = anno[0] + '.gif'

        while not os.path.exists(os.path.join(tgif_path, os.path.join("gifs", gif_path))):

            random_index = random.randint(0, annotation_length)

            anno = tgif_test_annotation[i][random_index]

            gif_path = anno[0] + '.gif'
        
        frame, question, multi_choice, answer = get_tgif_item(tgif_path, anno, anno_types[i])

        plt.subplot(4, 2, 2*i+1, xticks=[], yticks=[])
        plt.imshow(frame)

        plt.text(frame.width + 10, frame.height * 0.1, "Type: "+anno_types[i], fontdict=font)
        plt.text(frame.width + 10, frame.height * 0.23, "Q: "+question.capitalize(), fontdict=font)

        if(len(multi_choice) == 0):
            plt.text(frame.width + 10, frame.height * 0.36, "Ans: "+answer.capitalize()  , fontdict=font)
        
        else:
            option = ["A","B","C","D","E"]
            for j in range(len(multi_choice)):
                plt.text(frame.width + 10, frame.height * (0.36 + 0.13*j), "    "+option[j]+": "+multi_choice[j].capitalize()  , fontdict=font)
            plt.text(frame.width + 10, frame.height * (0.49 + 0.13*j), "Ans: "+answer.capitalize()  , fontdict=font)
        #print(question, answer)
    
    plt.show()

