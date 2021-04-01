# -*- coding: utf-8 -*-
"""
@Author : Horizon
@Date   : 2021-03-30 21:03:18
"""

import os
import sys
import json
import random
import numpy as np

from PyQt5.Qt import QFrame
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from mainwindow import Ui_MainWindow

class My_Window(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Video Question Answering Dataset Visualization")

        self.support_dataset = ["MSVD-QA", "MSRVTT-QA", "tgif-qa"]
        self.dataset_found = []        

        self.answer_label_list = [self.label_A, self.label_B, self.label_C, self.label_D,self.label_E]
        self.answer_option_list = ["A", "B", "C", "D", "E"]
        self.current_dataset = None
        self.player_activate_flag = False
        self.gif_activate_flag = False

        for answer_label in self.answer_label_list:
            answer_label.setFrameShape(QFrame.Box)

        self.vw = QVideoWidget(self.widget)
        self.vw.resize(640, 360)

        self.pushButton_search.clicked.connect(self.search_dataset)
        self.pushButton_refresh.clicked.connect(self.refresh)
        self.pushButton_callback.clicked.connect(self.callback)
        self.comboBox_dataset.currentIndexChanged.connect(self.change_dataset)
    
    def play_video(self, video_path):

        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.vw)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.player.play()
    
    def search_dataset(self):

        self.all_dataset_path = self.lineEdit_dataset_path.text()

        self.dataset_found = []
        self.comboBox_dataset.clear()
        self.comboBox_dataset.addItem("未选中")        

        for dataset in self.support_dataset:
            if(os.path.exists(os.path.join(self.all_dataset_path, dataset))):
                self.dataset_found.append(dataset)
                self.comboBox_dataset.addItem(dataset)
    
    def change_dataset(self):

        self.current_dataset = self.comboBox_dataset.currentText()

        self.dataset_path = os.path.join(self.all_dataset_path, self.current_dataset)

        if self.player_activate_flag:
            self.player.stop()
        
        if self.gif_activate_flag:
            self.gif.stop()

        if(self.current_dataset == "MSVD-QA" or self.current_dataset == "MSRVTT-QA"):

            self.player_activate_flag = True

            self.comboBox_type.clear()           

            val_annotation_path = os.path.join(self.dataset_path, "val_qa.json")

            with open(val_annotation_path) as f:
                self.annotation = json.load(f)
            
            self.annotation_length = len(self.annotation)
        
        elif(self.current_dataset == "tgif-qa"):

            self.gif_activate_flag = True

            self.comboBox_type.addItems(["action", "count", "frameqa", "transition"])

            tgif_test_action_annotation_path     = os.path.join(self.dataset_path, "Test_action_question.csv"    )
            tgif_test_count_annotation_path      = os.path.join(self.dataset_path, "Test_count_question.csv"     )
            tgif_test_frameqa_annotation_path    = os.path.join(self.dataset_path, "Test_frameqa_question.csv"   )
            tgif_test_transition_annotation_path = os.path.join(self.dataset_path, "Test_transition_question.csv")
            
            self.tgif_test_action_annotation     = np.loadtxt(tgif_test_action_annotation_path    , dtype=str, delimiter='\t')
            self.tgif_test_count_annotation      = np.loadtxt(tgif_test_count_annotation_path     , dtype=str, delimiter='\t')
            self.tgif_test_frameqa_annotation    = np.loadtxt(tgif_test_frameqa_annotation_path   , dtype=str, delimiter='\t')
            self.tgif_test_transition_annotation = np.loadtxt(tgif_test_transition_annotation_path, dtype=str, delimiter='\t')

        self.refresh()


    
    def callback(self):
        
        if(self.current_dataset == "MSVD-QA" or self.current_dataset == "MSRVTT-QA"):
            self.player.setPosition(0)
            self.player.play()
    
    def refresh(self):

        for answer_label in self.answer_label_list:
            answer_label.setStyleSheet("color:black")
            answer_label.setText(" ")

        if(self.current_dataset == "MSVD-QA" or self.current_dataset == "MSRVTT-QA"):

            self.comboBox_type.clear()                

            random_index = random.randint(0, self.annotation_length-1)

            random_anno = self.annotation[random_index]

            question = random_anno['question']
            answer = random_anno['answer']
            video_id = random_anno['video_id']

            if(self.current_dataset == "MSVD-QA"):
                video_path = os.path.join(self.dataset_path, "video/vid{}.avi".format(video_id))
            else:
                video_path = os.path.join(self.dataset_path, "video/video{}.mp4".format(video_id))

            self.textBrowser_question.clear()
            self.textBrowser_question.append(question.capitalize())
            self.label_A.setText(answer.capitalize())
            self.play_video(video_path)
        
        elif(self.current_dataset == "tgif-qa"):

            qa_type = self.comboBox_type.currentText()

            if(qa_type == "action"):
                self.annotation = self.tgif_test_action_annotation
            elif(qa_type == "count"):
                self.annotation = self.tgif_test_count_annotation
            elif(qa_type == "frameqa"):
                self.annotation = self.tgif_test_frameqa_annotation
            elif(qa_type == "transition"):
                self.annotation = self.tgif_test_transition_annotation

            self.annotation_length = len(self.annotation)

            random_index = random.randint(0, self.annotation_length-1)

            random_anno = self.annotation[random_index]

            gif_path = random_anno[0] + '.gif'

            while not os.path.exists(os.path.join(self.dataset_path, os.path.join("gifs", gif_path))):

                random_index = random.randint(0, self.annotation_length-1)

                random_anno = self.annotation[random_index]

                gif_path = random_anno[0] + '.gif'

            if(qa_type == "action" or qa_type == "transition"):

                question = random_anno[1]
                multi_choice = random_anno[2:7]
                answer = int(random_anno[7])
            
            elif(qa_type == "count" or qa_type == "frameqa"):

                question = random_anno[1]
                multi_choice = []
                answer = random_anno[2]

            self.textBrowser_question.clear()
            self.textBrowser_question.append(question.capitalize())

            if(len(multi_choice) != 0):
                for i, answer_label in enumerate(self.answer_label_list):
                    if(i == answer):
                        answer_label.setStyleSheet("color:red")
                    else:
                        answer_label.setStyleSheet("color:black")
                    answer_label.setText(self.answer_option_list[i] + ". " + multi_choice[i].capitalize())
            else:
                self.label_A.setText(answer.capitalize())
            
            self.gif = QMovie(os.path.join(self.dataset_path, os.path.join("gifs", gif_path)))
            self.label_frame.setMovie(self.gif)
            self.gif.start()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    MainWindow = My_Window()
    
    MainWindow.show()
    
    sys.exit(app.exec_())