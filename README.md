# attendance [![Build Status](https://travis-ci.org/team8/attendance.svg?branch=master)](https://travis-ci.org/team8/attendance)
##What is this?
This is an attendance system we are working on to benefit our robotics team, FRC Team \#8. We are currently working with a combination of [Django](https://www.djangoproject.com/), a Python library designed (well, for a lot of things) to make working with databases a bit easier; HTML; and some PHP for the online portal we're creating.

##How does it work?
WE HAVE NO IDEA. OH MY GOD, IT STARTED WORKING ON IT'S OWN. GOD FORGIVE US. WE CANNOT STOP THE MONSTROUSITY IT HAS BECOME. We are currently planning to use a Raspberry Pi to serve as the login/logout terminal for the students. We currently have the Pi inside a little wooden box that we made for a previous attendance system. We designed our box with an attached barcode scanner, so the login process is as simple as pulling out one's student ID card and scanning it (a numeric keypad is provided in the case a student forgets their ID card). From there, the scanner inputs the ID# encoded on the card to the database, and the site tells the user if they have logged in, or if they are logging out, it lets them know how many hours they have logged.

##Previous attendance system?
Yep. One of our contributors made an attendance system (that the team is currently using) in under a month as his Eagle Project. Since there was very little time for development, they ended up using Google Spreadsheets as a makeshift "backend", and a cannibalized Google Form for input. Obviously, this is not ideal for a variety of reasons, and this is why that we are working on this new system.

##Final Goal
Our final goal with this attendance system is to have a system in our lab, and an online portal.  The attendance system in the lab will be able to log people in and log out.  Online, people will be able to view their hours, log themselves in and out, and more!
