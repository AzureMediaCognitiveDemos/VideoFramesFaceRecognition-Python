# VideoFramesFaceRecognition
Video Frames Face Recognition Samples


## Preparation

### Create faceapi person group
```
./cogutils/create_persongroup.sh <personGroupId> <groupName>
```

For example, suppose personGroupId is 'demo_nogizaka46', and groupName is 'DEMO NOGIZAKA46', the command is like this:
```
./cogutils/create_persongroup.sh demo_nogizaka46 'DEMO NOGIZAKA46'
```

### Create peopleinput.csv
peopleinput.csv is an initial file that need to be created at under 'BATCH_WORK_DIR' directory.
The format of peopleinput.csv is


| Face Image URL                 | Face Name | Master Flag (0/1) |
|:------------------------------:|:---------:|:-----------------:|
| http://imgserver.com/face1.jpg | facename1 | 1                 |
| http://imgserver.com/face2.jpg | facename2 | 1                 |
| ...                            | ...       | 1                 |
| http://imgserver.com/faceN.jpg | facenameN | 0                 |



### Setup Azure Media Processors Modules
check out github repo and build the module in order to make it ready for batch execution
```
cd mediaprocessors
./setup.sh
```

## Batch execution

### run-batch command Usages
```
USAGE: ./run-batch [WORKFLOW] [BATCH_NAME] [BATCH_WORK_DIR] [PARAMS]
   WORKFLOW : ALL|REGIST_PEOPLE|GEN_FRAME|IDENTIFY
   PARAMS for each workflow
      REGIST_PEOPLE => [PERSON_GROUP_ID]
      ex) ./run_batch REGIST_PEOPLE mybatch /mybatch-work-dir my_person_group_id
      GEN_FRAME => [VIDEO_FILE]
      ex) ./run_batch GEN_FRAME mybatch /mybatch-work-dir /myvideo-path/myvideo.mp4
      IDENTIFY => [PERSON_GROUP_ID]
      ex) ./run_batch IDENTIFY mybatch /mybatch-work-dir my_person_group_id
      ALL => [PERSON_GROUP_ID] [VIDEO_FILE]
      ex) ./run_batch ALL mybatch /mybatch-work-dir my_person_group_id /myvideo-path/myvideo.mp4
```

### run all workflows example
```
./run-batch ALL nogizaka46 ../demo/nogizaka46 demo_nogizaka46 
```


### run regist people faces example
```
./run-batch REGIST_PEOPLE nogizaka46 demo_nogizaka46 ../demo/nogizaka46
created person: person_id (1) => 02bd629a-97fa-4dc7-8caa-6d06d429625e
created person: person_id (2) => c6311be8-71b3-42f8-8ff7-e406633ecfa5
created person: person_id (3) => bd7b8508-3ca3-47b3-8e29-3eeecd844946
created person: person_id (4) => 0d264abc-e648-46f1-a619-c3fef9cca719
created person: person_id (5) => ce8d90ac-b1b0-4020-a0fc-43425764d1fa
created person: person_id (6) => 5f0f8897-c37a-4e85-bb44-3cb0e74fbfd2
created person: person_id (7) => aa2c1b0c-6826-4984-9e6c-a3b111cde464
created person: person_id (8) => 383c3282-c412-400a-855a-39375c430e1c
created person: person_id (9) => 7b6f7932-b6b4-496c-8eb9-515dcc65e286
...
```

### generate frames
```
./run-batch GEN_FRAME nogizaka46 ../demo/nogizaka46 ../demo/nogizaka46/videos/The_Members_Introduction_Of_Nogizaka46_46_opv_46.mp4
```

### identify
```
./run-batch IDENTIFY nogizaka46 ../demo/nogizaka46 demo_nogizaka46 
```



