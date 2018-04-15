# BlueYonder
## Blue Yonder coding task

## Contents
+ [1. Introduction](#1-introduction)
+ [2. Examples](#2-list-of-examples)
+ [3. Build and deployment](#3-build-and-deployment)


## 0. Build badges

+ [![Code Health](https://landscape.io/github/pennyarcade/BlueYonder/master/landscape.svg?style=flat)](https://landscape.io/github/pennyarcade/BlueYonder/master)
+ [![Run Status](https://api.shippable.com/projects/5ac5bda72b913807002b59ea/badge?branch=master)](https://app.shippable.com/github/pennyarcade/BlueYonder) 
+ [![Coverage Badge](https://api.shippable.com/projects/5ac5bda72b913807002b59ea/coverageBadge?branch=master)](https://app.shippable.com/github/pennyarcade/BlueYonder) (Shippable)
+ [![Coverage Status](https://coveralls.io/repos/github/pennyarcade/BlueYonder/badge.svg?branch=master)](https://coveralls.io/github/pennyarcade/BlueYonder?branch=master) (Coveralls)


## 1. Introduction
+ [1.1 Coding Task](#11-coding-task)
+ [1.2 Development stack](#12-development-stack-used)
+ [1.3 Git repository structure](#13-git-repository-structure)
+ [1.4 Used python libraries](#14-used-python-libraries)
+ [1.5 Project directory structure](#15-project-directory-structure)
+ [1.6 License and 3rd party material](#16-license-and-3rd-party-material)
+ [1.7 Requirements to run these examples](#17-requirements-to-run-these-examples)

[Start of document](#contents) - [Start of chapter](#1-introduction)



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

[Start of document](#contents) - [Start of chapter](#1-introduction)

### 1.2 Development stack used

Here is a short overview of the software used in development. For services I would usually find in a corporate 
IT Infrastructure I am substituting free online services. I will add my favourite tools for professional use in brackets.

* IDE: Jetbrains PyCharm
* Scource code management: git, github
* Operating System: Ubuntu Mate 16.10
* Python virtual environment
* Virtualisation: Vagrant + VirtualBox; Configuration generated with puPHPet
* Unittests: Nosetests
* Dependency Management: PIP
* API Documentation: Epydoc
* Code duplication detection: clonedigger
* Quality management: Prospector / landscape.io (Prospector + CI Tool, landscape.io)
* Coverage reporting: Nosetests / coveralls.io (Nosetests + CI Tool, coveralls.io)
* Continuous integration/Deployment: shippable.com (Jenkins, Atlassin Bamboo)
* Hosting: pythonanywhere.com (Server with Debian/Ubuntu, Apache/Ngnx Webserver, MySQL/MariaDB Database )
* Issue management/Work organisation: Github Issues (OpenProject, Redmine, Atlassin Jira)

[Start of document](#contents) - [Start of chapter](#1-introduction)


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

[Start of document](#contents) - [Start of chapter](#1-introduction)
     
      
### 1.4 Used python libraries

This covers only major libraries and omits their dependencies for brevity

+ General
    + 3rd party libraries
        + nose - unit tests
        + prospector - run all major python code quality management tools
        + clonedigger - check for code duplication
        + epydoc - API Documetation generator
        + testfixtures - among others Log capturing in unittests
        + httpmock - mock http connections for unittests
+ Quick and dirty
    + Standard library
        + sys - for standard output
        + urllib - to parse url strings
        + os - to use line separator constant
    + 3rd party Libraries
        + requests - simplify web requests
+ Simple and Solid
    + Standard library
        + argparse - comand line argument handling
        + logging - logging classes and constants
        + os - file handling
        + sys - access to console streams
        + tempfile - writing temporary files for write access test workaround
        + errno - OS error constants 
    + 3rd party libraries
        + requests - simplify web requests
        + yaml - yaml file parsing 
        + (file)magic - wrapper to libmagic; can guess file type

[Start of document](#contents) - [Start of chapter](#1-introduction)
                

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
+ test
    + holds all unittests
    + may be excluded from productive deployment
+ test/fixtures
    + external files used for testing
+ venv
    + holds the python virtual environment (Managed by PyCharm)
    + should not be committed to the repository

[Start of document](#contents) - [Start of chapter](#1-introduction)
 


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

[Start of document](#contents) - [Start of chapter](#1-introduction)


### 1.7 Requirements to run these examples
   
#### Epydoc documentation generator

To use the gui of Epydoc you may have to install the package `python-tk` on Debian based linux distributions with:
`sudo apt-get install python-tk`

As far as I could find out there is no way to install this library via pip.

#### Modul (file)magic
For this module a current version of `libmagic` has to be installed.

Before installing filemagic, the libmagic library will need to be availabile. To test this is the check for the presence 
of the file command and/or the libmagic man page in unix shells.
```
$ which file
$ man libmagic
```
On Debain based linux distributions install it with the `file` package:

`$ sudo apt-get install file`

On Mac OSX, Apple has implemented their own version of the file command. However, libmagic can be 
installed using homebrew or macports

```
$ brew install libmagic
$ port install file
```

After brew finished installing, the test for the libmagic man page should pass.

On Windows you'll need DLLs for libmagic. Sources of the libraries in the past have been File for Windows . 
You will need to copy the file magic out of `[binary-zip]\share\misc`, and pass its location to Magic(magic_file=...).

If you are using a 64-bit build of python, you'll need 64-bit libmagic binaries which can be found here: 
https://github.com/pidydx/libmagicwin64. Newer version can be found here: https://github.com/nscaife/file-windows.

[Start of document](#contents) - [Start of chapter](#1-introduction)


## 2. List of examples
+ [2.1 Quick and dirty](#21-quick-and-dirty)
+ [2.2 Cheated](#22-cheated)
+ [2.3 Simple but solid](#23-simple-but-solid)
+ [2.4 Expanded and versatile](#24-expanded-and-versatile)
+ [2.5 API Approach](#25-api-approach)
+ [2.6 Web Form Approach](#25-web-form-approach)
+ [2.7 Example image list page](#27-example-image-list-page)

[Start of document](#contents) - [Start of chapter](#2-list-of-examples)


### 2.1 Quick and dirty
This is basically the minimalist version I would do if I was unter time pressure or
doing a very rapid prototype/proof of concept. It relies on the excellent `requests` library 
to simplify server interaction.
It is to be run on the webserver that serves the images.

Main file: `./quickanddirty.py`

#### Pro:
+ it just took 20 minutes to write
+ very short and easy to read

#### Con:
+ hardcoded config
+ spaghetti code
+ no error handling
+ no input verification
+ basically untestable beyond trying it out
+ works only on the webserver that serves the downloaded images and may drain its resources
+ bare minimum features

[Start of document](#contents) - [Start of chapter](#2-list-of-examples)


### 2.2 Cheated

This is basically what I would do as a dev ops guy. It is the quickest approach and 
I can trust the Linux community to write reliable and efficient tools. 
It just makes an entry for wget in the cron tab. wget is a very versatile tool with a lot of features.
I include this solution for completeness and to show thinking out of the box.

Main file: `crontab.tab`

#### Pro:
+ no coding necessary
+ using standard linux tools
+ just one crontrab entry
+ very efficient and versatile

#### Con:
+ this is cheating as there is no coding and no Python involved
+ only customisable in terms of already included configuration options

[Start of document](#contents) - [Start of chapter](#2-list-of-examples)


### 2.3 Simple but solid

-work in progress-

This Example expands on the "quick and dirty" approach to make it reliable and testable while still keeping it as 
simple as possible (KISS principle). It does only the specific task with a minimum feature set but improves quality 
and reliability. I will still use a procedural approach here since it would introduce to much complexity to use a 
object oriented approach. 

main file: `simpleandsolid.py`

#### Pro:
+ still very simple and lean
+ error handling
+ unittests
+ more modular
+ input verification
+ logging
+ argument parsing and verification

#### Con:
+ restricted feature set
+ not as easy to expand and add features
+ works only on the webserver that serves the downloaded images and may drain its resources

[Start of document](#contents) - [Start of chapter](#2-list-of-examples)


### 2.4 Expanded and versatile

-coming soon-

This Example expands on the previous simple but solid approach and introduces the object oriented paradigm to 
further modularize the app, increase maintainability and expandability. Through different classes implementing the 
same interface functionality can easily be added/swapped. This versatility comes with the cost of increased complexity,  
time to implement and volume of code. For long term usage and maintenance this is the best option.

Tin the below class structure overview the first possible implementation represents the required feature from the 
coding task, the other entries list possibilities for expansion

#### Class structure
+ Controller
    + Contains the general app workflow and handling as well as the coordination of the other classes/modules
    + Possible implementations arise from the combination of the below implementations as well as a possible need 
      for user interaction
+ Configuration loader
    + Load and combine configuration from different sources
    + Possible implementations:
        + Command line argument parser
        + Yaml file loader
        + Ini file loader
        + XML file loader
        + database loader
+ Reader
    + Reads a list of URLs to be processed from a source
    + Possible sources:
        + local file
        + standatd input stream
        + remote data via HTTP
        + remote data via FTP
        + remote data via network share 
        + crawl a website to search for image links
        + from a database table
+ Downloader
    + Downloads the image files via different protocols
    + Possible options:
        + HTTP
        + HTTP with basic authentication   
        + HTTP with Oauth handshake
        + FTP
        + network share
+ Writer
    + Writes the downloaded files one by one or collectively to their destination
    + Possible options:
        + One by one to local file system
        + one by one to a remote location
        + one by one to a network share
        + one by one upload to an API endpoint
        + one by one uploadd to an upload form
        + collectively and compressed to an archive file
        + collectively utilizing rsync to a network share 
        + collectively utilizing rsync to a remote server via ssh
        + write to a database
        + chunked/paginated upload of e.g. 10 files at once
        
#### Pro:
+ easily maintainable
+ easily expandable
+ error handling
+ unittests
+ very modular
+ input verification
+ logging
+ argument parsing and verification
+ depending on the implementation different deployment scenarios become possible

#### Con:
+ more complex
+ much more program code
+ takes much longer to design and implement

[Start of document](#contents) - [Start of chapter](#2-list-of-examples)
    

### 2.5 API approach

-coming soon-

In this version the code is included into the web application and offers one or more API
to trigger the execution. For small jobs this can be run directly on the server request 
for larger jobs this should trigger an entry into a job queue. 

#### Pro:
+ can be deployed as part of the web application or stand alone
+ can be triggered and monitored remotely
+ uses the web server infrastructure
+ can make use of web framework or CMS capabilities

#### Con:
+ all restrictions of the webserver apply
+ additional request overhead / server load
+ needs a webserver to run

[Start of document](#contents) - [Start of chapter](#2-list-of-examples)


### 2.6 Web Form Approach

- coming soon -

This is basically the same as the API approach and can be combined with it. In addition to 
above example it offers a web form to upload/enter a list of urls and configuration to be easily
triggered manually. It shares the same pros and cons.

[Start of document](#contents) - [Start of chapter](#2-list-of-examples)


### 2.7 Example image list page

- optional -

A sample page to display the downloaded images

[Start of document](#contents) - [Start of chapter](#2-list-of-examples)



## 3. Build and deployment
+ [3.1 Local testing](#31-local-testing)
+ [3.2 Dev build](#31-dev-build)
+ [3.3 Stage build](#32-stage-build)
+ [3.4 Production build](#34-production-build)
+ [3.5 Build tools](#35-build-tools)

[Start of document](#contents) - [Start of chapter](#3-build-and-deployment)


### 3.1 Local testing

The local testing environment should make as much use of the IDE capabilities as possible. Unittests and code quality 
tools should be run  manually and regularly at least before committing. The Python environment should be wrapped in a 
virtual environment. If needed the server environment can be modelled with the help of vagrant.

[Start of document](#contents) - [Start of chapter](#3-build-and-deployment)


### 3.2 Dev build
This stage is optional and often ommited for small scale projects/teams. It runs unittests and quality management tools 
via the continuous integration solution to spot problems on the dev branch automatically with every commit. It should 
not be deployed automatically but may be deployed manually to showcase progress internally. 

[Start of document](#contents) - [Start of chapter](#3-build-and-deployment)


### 3.3 Stage build
The stage or prelive build is run by the CI system each time the dev branch is merged into the stage branch. It runs all
unit tests and quality management tools again to ensure high stability. This build is then automatically deployed to a 
stage server. There manual testing and quality assurance as well as automatical integration and end to end tests are 
performed to test the interaction with all other stage systems of the server infrastructure. 
This build can after quality management be frozen and showed to internal and external customers for approval.

[Start of document](#contents) - [Start of chapter](#3-build-and-deployment)


### 3.4 Production build
Only production ready, tested and approved code should be merged into the master branch wich holds the productive code.
The productive build and deployment differs very little from the stage build. The build time tests are run again as a 
last failsave. The master branch can be deployed automatically after a successful build but some teams prefer to trigger 
production deployments manually.
No integration tests are run on the production server. It is tightly monitored to ensure highest availability.

[Start of document](#contents) - [Start of chapter](#3-build-and-deployment)
 

### 3.5 Build tools
There aren't very many simple and efficient build tools in the python sphere. And most of the available options are 
lacking in one or more aspects. On the one hand you can just "git pull and pray" but leaving yourself open to build 
inconsistencies between servers. You can build python packages for pip but then have to rely on a pip server being 
available and 3rd party libraries as well as the environment are not included. There are different tools to build python 
executables but usually those are os dependent. You can try to adapt build tools from other languages which introduce 
unnecessary overhead and complexity. An more reliable way it to use a container build system like docker. That also 
carries a lot of overhead including its own server and is not available for all systems.  

The best was to deploy a python app including its environment I could find is a combination of a tool called 
_dh-virtualenv_ developed by Spotify and the python deploy tool _fabric_ wich seems to work very similar to a ruby based 
deploy tool I know called capistrano.

_dh-virtualenv_ bundles the complete virtual environment of one's app into a debian package. This package installs at
`/usr/share/python/<project-name>`. The deployment process just takes three simple steps:
+ upload the .deb package
+ run `dpkg -i`
+ reload/restart app/webserver if necessary
rollback is equally simple. Just install the previous package again. 

_fabric_ can automate this process further. It is a tool to run scripts on remote servers and is configured in python 
code. So it fits seamlessly into the Python development environment.

For larger numbers of servers the use of debian packages has further advantages. The system administrators are very 
familiar with their handling and it is pretty easy to host your own package repository.
When the package is deployed to a repository the servers just need to run one command to update packages from that 
repository. This can even happen as an automated task for example nightly when the server load is lowest. 

[Start of document](#contents) - [Start of chapter](#3-build-and-deployment)
