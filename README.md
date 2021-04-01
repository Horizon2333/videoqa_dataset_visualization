# Video question answering dataset visualization

Load and visualize different datasets in video question answering.

1. [Project structure](#project-structure)
2. [Dataset structure](#dataset-structure)
3. [Install](#install)
4. [Usage](#usage)
5. [Dataset](#dataset)
   * [MSVD-QA](#msvd-qa)
   * [MSRVTT-QA](#msrvtt-qa)
   * [tgif-qa](#tgif-qa)
6. [Result](#result)

## Project structure
```
$videoqa_dataset_visualization
    |──results              # result image
        |──msvd.png
        |──msrvtt.png
        |──tgif.png
        |──ui.png
    |──mainwindow.py        # ui file based on PyQt5
    |──mainwindow.ui        # can be modified with Qt Creator
    |──msvd_visualize.py    # msvd-qa dataset visualization
    |──msrvtt_visualize.py  # msrvtt-qa dataset visualization
    |──tgif_visualize.py    # tgif-qa dataset visualization
    |──ui.py                # use GUI to visualization above datasets
    |──vqa.png              # material picture
    |──requirements.txt
    |──README.md
```
## Dataset structure
```
$all_dataset_path
    |──MSVD-QA
        |──video
            |──vid1.avi
            |── ...
            |──vid1970.avi
        |──train_qa.json
        |──val_qa.json
        |──test_qa.json
    |──MSRVTT-QA
        |──video
            |──video0.mp4
            |── ...
            |──video9999.mp4
        |──train_qa.json
        |──val_qa.json
        |──test_qa.json
    |──tgif-qa
        |──gifs
            |──tumblr_lgkgapWO4E1qbjyiko1_500.gif
            |── ...
        |──Test_action_question.csv
        |──Test_count_question.csv
        |──Test_frameqa_question.csv
        |──Test_transition_question.csv
        |──Total_action_question.csv
        |──Total_count_question.csv
        |──Total_frameqa_question.csv
        |──Total_transition_question.csv
        |──Train_action_question.csv
        |──Train_count_question.csv
        |──Train_frameqa_question.csv
        |──Train_transition_question.csv
```


## Install

1. Clone the project
```shell
git clone https://github.com/Horizon2333/videoqa_dataset_visualization
cd videoqa_dataset_visualization
```
2. Install dependencies
```shell
pip install -r requirements.txt
```

## Usage
1.  Visualize individual dataset with matplotlib :

```shell
python msvd_visualize.py --path {your msvd-qa dataset path such as F:/Dataset/MSVD-QA}
python msrvtt_visualize.py --path {your msrvtt-qa dataset path such as F:/Dataset/MSRVTT-QA}
python tgif_visualize.py --path {your tgif-qa dataset path such as F:/Dataset/tgif-qa}
```

2. Use GUI to visualize different dataset:

```shell
python ui.py
```

## Dataset 

### MSVD-QA

Dataset size: ```~1.7G```

#### Download links

[MSVD Official link](https://www.cs.utexas.edu/users/ml/clamp/videoDescription/) ,
[MSVD video link](https://www.multcloud.com/share/050e69cd-cab9-4ba3-a671-ed459341ab41) (have a better name format),
[MSVD-QA annotation link](https://mega.nz/file/QmxFwBTK#Cs7cByu_Qo42XJOsv0DjiEDMiEm8m69h60caDYnT_PQ) 

#### Annotation 

Annotation format : ```dict```  stored in ```json``` file.

Loading annotation:

```
import json

with open("val_qa.json") as f:
    annotation = json.load(f)
```

The example of one annotation is like:
```
>>> annotation[0]
{'answer': 'someone', 'id': 30933, 'question': 'who pours liquid from a plastic container into a ziploc bag containing meat pieces?', 'video_id': 1201}
```

Get video name, question and answer:

```
video_name = 'vid' + annotation[index]['video_id'] + '.avi' 
# video_name = 'vid1201.avi'
question = annotation[index]['question']                    
# question = 'who pours liquid from a plastic container into a ziploc bag containing meat pieces?'
answer = annotation[index]['answer']
# answer = 'someone'
```

Then we can use video name and video path to load videos with the help of opencv.

### MSRVTT-QA

Dataset size: ```~6.3G```

#### Download links

[MSRVTT video and annotation link](https://www.mediafire.com/folder/h14iarbs62e7p/shared) ,
[MSRVTT-QA annotation link](https://mega.nz/file/UnRnyb7A#es4XmqsLxl-B7MP0KAat9VibkH7J_qpKj9NcxLh8aHg) 

#### Annotation 

There are only few differences between MSRVTT-QA dataset annotation and MSVD-QA dataset annotation.

Annotation format : ```dict```  stored in ```json``` file.

Loading annotation:

```
import json

with open("val_qa.json") as f:
    annotation = json.load(f)
```

The example of one annotation is like:

```
>>> annotation[0]
{'answer': 'couch', 'category_id': 14, 'id': 158581, 'question': 'what are three people sitting on?', 'video_id': 6513}
```

Get video name, question and answer:

```
video_name = 'video' + annotation[index]['video_id'] + '.mp4' 
# video_name = 'video6513.mp4'
question = annotation[index]['question']                    
# question = 'what are three people sitting on?'
answer = annotation[index]['answer']
# answer = 'couch'
```

Then we can use video name and video path to load videos with the help of opencv.

### tgif-qa

Dataset size: ```~123G```

#### Download links

[tgif-qa gif and annotation link](https://github.com/YunseokJANG/tgif-qa/tree/master/dataset) 

#### Annotation 

Dataset tgif-qa have 4 different types of QA pair, so the annotation format is also different.

Annotation format : ```array```  stored in ```csv``` file with delimiter ```\t```.

##### Action

Loading annotation:

```
import numpy as np

tgif_test_action_annotation = np.loadtxt("Test_action_question.csv", dtype=str, delimiter='\t')
```

The first line of the  ```csv``` is the content of different columns:

```
>>> tgif_test_action_annotation[0]
array(['gif_name', 'question', 'a1', 'a2', 'a3', 'a4', 'a5', 'answer', 'vid_id', 'key'], dtype='<U73')
```

The above output means that ```action``` is a multi-choice type task.

The example of one annotation is like:

```
>>> tgif_test_action_annotation[1]
array(['tumblr_nk172bbdPI1u1lr18o1_250',
       'What does the butterfly do 10 or more than 10 times ?',
       'stuff marshmallow', 'holds a phone towards face', 'fall over',
       'talk', 'flap wings', '4', 'ACTION4', '26'], dtype='<U73')
```

Get gif name, question and answer:

```
gif_name = tgif_test_action_annotation[index][0] + '.gif' 
# video_name = 'tumblr_nk172bbdPI1u1lr18o1_250.gif'
question = tgif_test_action_annotation[index][1]                    
# question = 'What does the butterfly do 10 or more than 10 times ?'
multi_choice = tgif_test_action_annotation[index][2:7]
# multi_choice = array(['stuff marshmallow', 'holds a phone towards face', 'fall over', 'talk', 'flap wings'], dtype='<U73')
answer = tgif_test_action_annotation[index][7]
# answer = '4', means correct answer is 'flap wings'.
```
##### Count

Loading annotation:

```
import numpy as np

tgif_test_count_annotation = np.loadtxt("Test_count_question.csv", dtype=str, delimiter='\t')
```

The first line of the  ```csv``` is the content of different columns:

```
>>> tgif_test_count_annotation[0]
array(['gif_name', 'question', 'answer', 'vid_id', 'key'], dtype='<U97')
```

The above output means that ```count``` is a open-ended type task.

The example of one annotation is like:

```
>>> tgif_test_count_annotation[1]
array(['tumblr_nezfs4uELd1u1a7cmo1_250',
       'How many times does the man adjust waistband ?', '3', 'COUNT12',
       '52'], dtype='<U97')
```

Get gif name, question and answer:

```
gif_name = tgif_test_count_annotation[index][0] + '.gif' 
# video_name = 'tumblr_nezfs4uELd1u1a7cmo1_250.gif'
question = tgif_test_count_annotation[index][1]                    
# question = 'How many times does the man adjust waistband ?'
answer = tgif_test_count_annotation[index][2]
# answer = '3'
```
##### Other

Type ```frameqa``` is like type ```count```.
Type ```transition``` is like type ```action```.

## Results

Visualize MSVD-QA:

![MSVD-QA](https://github.com/Horizon2333/videoqa_dataset_visualization/blob/main/results/msvd.png)

Visualize MSRVTT-QA:

![MSVD-QA](https://github.com/Horizon2333/videoqa_dataset_visualization/blob/main/results/msrvtt.png)

Visualize tgif-qa:

![MSVD-QA](https://github.com/Horizon2333/videoqa_dataset_visualization/blob/main/results/tgif.png)

Visualize GUI:

![MSVD-QA](https://github.com/Horizon2333/videoqa_dataset_visualization/blob/main/results/ui.png)

***

If there are something wrong with my code or any questions, please tell me, thanks a lot!

