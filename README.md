# Mini Project 3
## Useage
The purpose of **Mini project 3** is to manage data in **Mini project 1**. There are two databases used in this project.
> First is **MySQL**, it's a SQL database

> Second is **MongoDB**, it's a Non-SQL database

## What's new
1. Rewrite **Mini project 1** to redirect data to database, in two database respectively.
2. Write three API function for each database according to requirement.
## How to run this project
### Mini Project 1 Part
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
7. To start the whole program, run the ```start_here_MongoDB.bat``` or ```start_here_MySQL.bat```, to chose different database;
8. You may enter any argument you want when system ask you, but to test the project better and make sure it works, I suggest that you can always press the "Enter"key to use my default value, and it will also be easier for you to test my code;
9. If you want to run my project more than once, please delete all the files in folder "images"
10. I will show you the result and the process of running my code, so if there is any problem with my code, please send Issues to me, thanks.

### Mini Project 3 Part
1. Run ```MongoDB_API.py``` to test three API for MongoDB database, but first you need to have a valid collection which can let API work on.
2. Run ```MySQL_API.py``` to test three API for MySQL database, but first you need to have a valid table which can let API work on.

**P.S.** All these API are importable as libraries

**P.S.S** Remeber to replace the setting of database according to your own database before you run the code, I will hide my own password for security.

## Result Demo
I will post the result of my work as ```.txt``` file to demonstrate the result of **Mini Project 3**, which can show how my **Mini Project 3** can work associated with **Mini Project 1**.
All results are in the folder ```result```
### mongodb.txt
This file shows how the data acquired in **Mini Project 1** organized in MogoDB database.
### mysql.txt
This file shows how the data acquired in **Mini Project 1** organized in MySQL database.
### mongodb_api.txt
This file shows how APIs works in MogoDB database. The file contain the result of three APIs
1. find_session_with_word: Search for certain words and retrieve which user/session that has this work in it. 
2. num_of_image: Number of images per feed
3. most_popular_des: Find most popular descriptors
### mysql_api.txt
This file shows how APIs works in MySQL database. The file contain the result of three APIs
1. search_by_word: Search for certain words and retrieve which user/session that has this work in it. 
2. num_of_image: Number of images per feed
3. most_popular_des: Find most popular descriptors


