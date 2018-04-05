# BlueYonder
## Blue Yonder coding task


## 0. Build badges

+ [![Code Health](https://landscape.io/github/pennyarcade/BlueYonder/master/landscape.svg?style=flat)](https://landscape.io/github/pennyarcade/BlueYonder/master)
+ [![Run Status](https://api.shippable.com/projects/5ac5bda72b913807002b59ea/badge?branch=master)](https://app.shippable.com/github/pennyarcade/BlueYonder) 
+ [![Coverage Badge](https://api.shippable.com/projects/5ac5bda72b913807002b59ea/coverageBadge?branch=master)](https://app.shippable.com/github/pennyarcade/BlueYonder) (Shippable)
+ [![Coverage Status](https://coveralls.io/repos/github/pennyarcade/BlueYonder/badge.svg?branch=master)](https://coveralls.io/github/pennyarcade/BlueYonder?branch=master) (Coveralls)


## 1. Introduction

### 1.1 Coding Task

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


### 1.2 Development stack used

Here is a short overview of the software used in development. For services I would usually find in a corporate 
IT Infrastructure I am substituting free online services. I will add my favourite tools for professional use in brackets.

* IDE: Jetbrains PyCharm
* Scource code management: git, github
* Operating System: Ubuntu Mate 16.10
* Python virtual environment
* Virtualisation: Vagrant + VirtualBox
* Unittests: Nosetests
* Dependency Management: PIP
* API Documentation: Epydoc
* Code duplication detection: clonedigger
* Quality management: Prospector / landscape.io (Prospector + CI Tool, landscape.io)
* Coverage reporting: Nosetests / coveralls.io (Nosetests + CI Tool, coveralls.io)
* Continuous integration/Deployment: shippable.com (Jenkins, Atlassin Bamboo)
* Hosting: pythonanywhere.com (Server with Debian/Ubuntu, Apache/Ngnx Webserver, MySQL/MariaDB Database )
* Issue management/Work organisation: Github Issues (OpenProject, Redmine, Atlassin Jira)


### 1.3 Git repository structure
Here is how I usually structure my code repository to facilitate a fluent coding experience in a team.
There are 3 main branches:
* master: all code in master is tested, stable and ready for production deployment
    * If needed there can be tags to signify deployed versions
    * merged from next after approval
* next: stage branch to be deployed to a prelive, staging server. The code here should be largely stable and ready for 
        review, final testing and approval
    * merged from dev after a development cycle and submitted for review
* dev: Branch for local development and testing. The code here is altered regularly and may not always be stable 
       (although all developers should strive to omit committing broken code)
    * If needed and for larger teams one should use feature branches for individual development. For small projects or 
      single developers this may add too much complexity/overhead
     
      
### 1.4 Used python libraries

This covers only major libraries and omits their dependencies for brevity

+ General
    + 3rd party libraries
        + nose - unit tests
        + prospector - run all major python code quality management tools
        + clonedigger - check for code duplication
        + epydoc - API Documetation generator
+ Quick and dirty
    + Standard library
        + sys - for standard output
        + urllib - to parse url strings
        + os - to use line separator constant
    + 3rd party Libraries
        + requests - simplify web requests
+ Simple and Solid
    + Standard library
    + 3rd party libraries
        + requests - simplify web requests
        + argparse - comand line argument handling
        

### 1.5 Project directory structure

Here is the directory layout of this sample project. It diverts a little from an ideal structure because 
I include multiple examples in one project

+ project root
    + README
    + LICENSE
    + web service / build configuration
    + main application file, run this to start the corresponding example app
+ config
    + the application's config files go here
    + you may symlink a different directory here tp persist configuration 
      over different deployed versions
    + be sure not to commit sensitive authentication data to git
      (I may be breaking this rule for less sensitive data for convenience here)
+ docs
    + automatically generated API documentation
    + may be excluded from productive deployment
+ inbox
    + directory to hold the (sample) input files
+ logs
    + all application logs go here.
    + in a production environment one may choose to configure the 
      system's log directory or symlink another location
+ metrics
    + colds code metric reports generated manually or by CI
    + should be excluded from productive deployment
+ tests
    + holds all unittests
    + may be excluded from productive deployment
+ venv
    + holds the python virtual environment (Managed by PyCharm)
    + should not be committed to the repository
 


### 1.6 License and 3rd party material

An overview over the licensing of the materials used

+ Own code
    + I chose the MIT License for my code because it is simple and short and to comply with open source 
    requirements for the web services used             
+ Development stack
    + PyCharm is a proprietary IDE. I am using the free Community edition but 
    would prefer the professional product line for work on the job
    + The web servics employed all need to be licensed and payed for for commercial use
      but offer free accounts for open source projects (public repositories)
    + all other software is licensed under different open source licenses and free 
      to use commercially to the best of my knowledge
+ 3rd party libraries
    + all libraries are licensed under different open source licenses and free 
      to use commercially to the best of my knowledge
+ Sample images
    + I will be using sample images, urls and pages from https://www.pexels.com 
    for testing and demonstration which are licensed under Creative Commons Zero (CC0) license  


### 1.7 Optional requirements
   
   To use the gui of Epydoc you may have to install the package `python-tk` with:
   `sudo apt-get install python-tk`
   
   As far as I could find out there is no way to install this library via pip.


## 2. List of examples
+ Quick and dirty
+ Cheated
+ Simple but solid
+ Expanded and versatile
+ API Approach
+ Web Form Approach
+ Example image list page
+ Example image source page


### 2.1 Quick and dirty
This is basically the minimalist version I would do if I was unter time pressure or
doing a very rapid prototype/proof of concept. It relies on the excellent `requests` library 
to simplify server interaction.
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
* bare minimum features


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


### 2.3 Simple but solid

This Example expands on the "quick and dirty" approach to make it reliable and testable while still keeping it as 
simple as possible (KISS principle). It does only the specific task with a minimum feature set but improves quality 
and reliability. I will still use a procedural approach here since it would introduce to much complexity to use a 
object oriented approach. 

main file: `simpleandsolid.py`

#### Pro:
* still very simple and lean
* error handling
* unittests
* more modular
* input verification
* logging
* argument parsing and verification

#### Con:
* restricted feature set







## 3. Build and deployment

### 3.1 Local testing



### 3.2 Dev build



### 3.3 Stage build



### 3.4 Stage deployment



### 3.5 Production build



### 3.6 Production deployment



