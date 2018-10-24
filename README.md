# work-for-EC601
Let's make the most simple instruction in case of that I'm running out of time.
## How to run this project
1. First you should create a folder and download all the files in this project into this folder(video may not be necessary);
2. Put your Google cloud credential(the json file) into this this folder;
3. Creat a text file in this folder and copy your twitter credential into this file 
make sure that you paste your keys and token with the following format(without quote):
```javascript
(API key)
(API secret key)
(Access token)
(Access token secret)
```
make sure that you copy and paste, only paste your those four strings to each line as the same order as mentioned, without anything else, including space;

4. Edit 'start_here.bat', replace the content behide "=" by your google credential file name, without space, as following;
```javascript
set GOOGLE_APPLICATION_CREDENTIALS=My Project 27058-f61d3c8b09ce.json
```
5. Edit 'myprojectcode.py', go to the line 280, replace the name of twitter credential file(created in step.3) by yours;
6. Create an empty folder named "images" in the current folder;
7. To start the whole program, run the 'start_here.bat';

test for -
-----------------------------------------------
8. You may enter any argument you want when system ask you, but to test the project better and make sure it works, I suggest that you can always press the "Enter"key to use my default value, and it will also be easier for you to test my code;
9. If you want to run my project more than once, please delete all the files in folder "images"
10. I will show you the result and the process of running my code, so if there is any problem with my code, please send Issues to me, thanks.

