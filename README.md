# BlueYonder
## Blue Yonder coding task

### 1. Task

As first step of the Blue Yonder hiring process, we kindly ask applicants to hand in a solution to the small programming task below to demonstrate their professional approach to developing software. For us, this includes appropriate unit tests and the application of clean code principles. We value both technical correctness and coding style.
Please be assured that there is no time limit, so you are free to tackle this task whenever it suits you best. Enjoy coding, we are looking forward to receive your response. If we like your solution, we will invite you for interviews, where we will also talk with you about your code.
If you have any questions, please do not hesitate to contact us.
Kind regards
Team Platform

---

Given a plaintext file containing URLs, one per line, e.g.:

```
http://mywebserver.com/images/271947.jpg
http://mywebserver.com/images/24174.jpg
http://somewebsrv.com/img/992147.jpg
```

Write a script that takes this plaintext file as an argument and downloads all images, storing them on the local hard disk. Approach the problem as you would any task in a normal day’s work. Imagine this code will be used in important live systems, modified later on by other developers, and so on.
Please use the Python programming language for your solution. We prefer to receive your code in GitHub or a similar repository.
In a deployment scenario this script needs to be deployed to multiple Debian machines, scheduled to run every five minutes. The downloaded images should be served via http on each server.
Provide an example deployment or instructions with your solution.

### 2. List of examples
+ Quick and dirty
+ Cheated
+ Simple but solid
+ Expanded and versatile
+ Cron Job Approach
+ API Approach
+ Web Form Approach
+ Example image list page

### 2.1 Quick and dirty
This is basically the minimalist version I would do if I was unter time pressure or
doing a very rapid prototype/proof of concept. 
It is to be run on the webserver that serves the images.

Main file: `./quickanddirty.py`

#### Pro:
* it just took 20 minutes to write
* very short and easy to read

#### Con:
* hardcoded config
* spaghetti code
* no error handling
* no input verification
* basically untestable beyond trying it out
* works only on the webserver that serves the downloaded images and may drain its resources

### 2.2 Cheated

This is basically what I would do as a dev ops guy. It is the quickest approach and 
I can trust the Linux community to write reliable and efficient tools. 
It jut makes an entry for wget in the cron tab. wget is a very versatile tool with a lot of features.
I include this solution for completeness and to show thinking out of the box.

Main file: `crontab.tab`

#### Pro:
* no coding necessary
* using standard linux tools
* just one crontrab entry
* very efficient and versatile

#### Con:
* this is cheating as there is no coding and no Python involved


