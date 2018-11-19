This is the README file for yl4785's Assigment Three for Application Security. 

The following instruction is for MAC users:

In order to run this web application, there are some things you must do to prepare the ideal environment. 

One of the first things you need to do is to make sure you have Python downloaded. To check this, you can just type python in your shell, where you should see some code that resembles the following: 

Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>

If you do not have Python already installed, you can download the latest version from this link: 
https://www.python.org/downloads/

Once Python is downloaded, you're going to want to install pip if you do not have it already. pip is an easy to use installer for packages. If you do have pip and you find out it is outdated, your shell will provide you with directions for how to update pip. 

After pip is installed, you are going to want to download virtualenv. Virtualenv provides you with an isolated Python environment, which is more practical than installing packages systemwide and also allow you to install packages without administrator privileges. you can visit this webpage: http://flask.pocoo.org/docs/0.12/installation/  where it will tell you to do the following:

$ sudo pip3 install virtualenv

Once you have virtualenv installed, just open a shell and create your own environment. you can create a project folder and a venv folder within:

$ mkdir your_file_name
$ cd your_file_name
$ virtualenv venv

Then to activate the corresponding environment. On OS X and Linux do: $ source venv/bin/activate. Once the above is done, it is time to download Flask. To do so, you just need to enter the command pip install Flask（or pip3 install Flask if you installed Python3 in your labtop） in the shell prompt. To verify that, Flask can be seen by Python, type python into your shell. Then at the Python prompt, try to import Flask. 

>>> import flask
If there is no error, then you are good to go.To exit out of the Python prompt, simply type quit().
Once Flask is on the machine, you should to install some Flask extensions which are packages that adds the specific functionality to a Flask app. To add functionality for web forms, we'll use Flask-WTF.  First, get back into the apps. Isolate the Python development environment(type source venv/bin/activate). Next, use pip3 to install Flask-WTF.And downloading OpenCV since we will be using it to interact with the images. To do this, type the command pip3 install opencv-python. 

We also need a place to safely store a user's data which is a database. In this assignment, I use PostgreSQL as a relational database to store the flask app's data.To install Postgres, go to postgresql.org/download and follow the instructions for your operating system. I used an app called Postgres.app, which I found on this download page for Mac. Once you download Postgres, you'll need to create a new user account and password and sign in. Then get back into the isolated Python development environment and use pip3 to install Flask-SQLAlchemy.

Once done, you need to run routes.py file, this will allow you to see the pages on your browser. To see the pages, copy the IP address the shell gives you: http://127.0.0.1:5000/

Mannual for web users:

This is the Squaring Image Web Application Interface with a signup/login frontend accompanied by web vulnerabilities. First,you see three buttons on the main page:Sign up, Log in and Learn more button. If you have already signed up for an account then choose Log in button and fill in your actual email address with correct password to access to the home page where you can upload,modify and see your own pictures.Otherwise, you need to click on the Sign up button and create an valid account first, in this case you need to provide the information of your First name, Last name, Email address as well as Password,this web app contains a basic validator named Data Required to check that the field is filled in and it is the right format. If any validation check fails the signup page should reload with a helpful error message so that the user can fix the mistake and try again. When you log into the home page, you just need to select your image file, choose the resizing mode (use side length / use ratio), and input your parameter. This web could enlarge or shrink the images. After submitting the image and parameters, you will be allowed to download the image squared in png format. In the upload page or download page, you can jump to the main page in any time by clicking on the Logout button.



# logging-squaring-app
