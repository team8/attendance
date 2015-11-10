# attendance

##What is this?
This is an attendance system we are working on to benefit our robotics team, FRC Team \#8. We are currently working with a combination of [Django](https://www.djangoproject.com/), a Python library designed (well, for a lot of things) to make working with databases a bit easier; HTML; and some PHP for the online portal we're creating.

##How does it work?
Our plan is to use a little box that we made for a previous attendance system (more on that later), and just modify the startup process so the Pi goes directly to our attendance login page. We designed our box with an attached barcode scanner, so the login process is as simple as pulling out one's student ID card and scanning it (a numeric keypad is provided in the case a student forgets their ID card). From there, the scanner inputs the ID# encoded on the card to the database, and the site tells the user if they have logged in, or if they are logging out, it lets them know how many hours they have logged.

##Previous attendance system?
Yep. One of our contributors made an attendance system (that the team is currently using) in under a month as his Eagle Project. Since there was very little time for development, they ended up using Google Spreadsheets as a makeshift "backend", and a cannibalized Google Form for input. Obviously, this is not ideal for a variety of reasons, and this is why that we are working on this new system.
