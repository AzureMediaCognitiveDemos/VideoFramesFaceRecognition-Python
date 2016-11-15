# VideoFramesFaceRecognition
Video Frames Face Recognition Samples

![Screenshot build 2016 Keynote](https://raw.githubusercontent.com/AzureMediaCognitiveDemos/VideoFramesFaceRecognition-Python/master/img/screenshot-build2016keynote.jpg)

Demo: [http://aka.ms/amcdemo_videoface](http://aka.ms/amcdemo_videoface)

## 1. Preparation

### 1-1. Configurations for Azure Services
You have to create the following Azure services accounts and configure the files for each service:

| Azure Services                | Config file    | 
|-------------------------------|----------------|
| Azure Media Services          | ams.conf       |
| Azure Storage (x)             | storage.conf   |
| Cognitive Services (faceapi)  | cognitive.conf | 
(x) - Azure Storage account here has to be the one that is attached to Azure Media Services account here.

### 1-2. Create faceapi person group
```
./cogutils/create_persongroup.sh <personGroupId> <groupName>
```

For example, suppose personGroupId is 'build2016keynote', and groupName is 'DEMO Build 2016 Keynote', the command is like this:
```
./cogutils/create_persongroup.sh build2016keynote 'DEMO Build 2016 Keynote'
```

### 1-3. Create peopleinput.csv
peopleinput.csv is an initial file that need to be created at under 'BATCH_WORK_DIR' directory.
The format of peopleinput.csv is


| Face Image URL                 | Face Name | Master Flag (0/1) |
|:------------------------------:|:---------:|:-----------------:|
| http://imgserver.com/face1.jpg | facename1 | 1                 |
| http://imgserver.com/face2.jpg | facename2 | 1                 |
| ...                            | ...       | 1                 |
| http://imgserver.com/faceN.jpg | facenameN | 0                 |

See sample [peopleinput.csv](https://github.com/AzureMediaCognitiveDemos/VideoFramesFaceRecognition/blob/master/demo/build2016keynote/peopleinput.csv) 


### 1-4. Setup Azure Media Processors Modules
Please install maven and git if not yet installed on your environment
```
# for Ubuntu/Debian
sudo apt-get install git
sudo apt-get install maven

# for CentOS
sudo yum install git
sudo yum install maven
```

Check out github repo and build the module in order to make it ready for batch execution
```
cd mediaprocessors
./setup.sh
```

## 2. Batch execution

### run-batch command Usages
```
usage: ./run-batch [WORKFLOW] [BATCH_NAME] [BATCH_WORK_DIR] [PARAMS]
This program generates webvtt file from your video and people master 
that you register leveraging Azure Media Services and Cognitive Services

WORKFLOW:  ALL|REGIST_PEOPLE|GEN_FRAME|IDENTIFY
PARAMS for each WORKFLOW:
  REGIST_PEOPLE => [PERSON_GROUP_ID]
    ex)  ./run_batch REGIST_PEOPLE mybatch /mybatch-work-dir my_person_group_id
  GEN_FRAME => [VIDEO_FILE]
    ex)  ./run_batch GEN_FRAME mybatch /mybatch-work-dir /myvideo-path/myvideo.mp4
  IDENTIFY => [PERSON_GROUP_ID]
    ex)  ./run_batch IDENTIFY mybatch /mybatch-work-dir my_person_group_id
  ALL => [PERSON_GROUP_ID] [VIDEO_FILE]
    ex)  ./run_batch ALL mybatch /mybatch-work-dir my_person_group_id /myvideo-path/myvideo.mp4
```

### Example1: Run all workflows
```
./run-batch ALL build2016keynote ../demo/build2016keynote demo_build2016keynote
```


### Example2: Run each workflow one by one

```
# regist people faces example
./run-batch REGIST_PEOPLE nogizaka46 demo_build2016keynote ../demo/build2016keynote

# generate frames
./run-batch GEN_FRAME build2016keynote ../demo/build2016keynote ../demo/build2016keynote/videos/build2016keynote.mp4

# identify
./run-batch IDENTIFY build2016keynote ../demo/build2016keynote demo_build2016keynote
```

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/AzureMediaCognitiveDemos/VideoFramesFaceRecognition-Python.

