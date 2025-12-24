# Pikafood
#### Video Demo: https://youtu.be/JFwH7OAu0FY

## Description:

### Intro:
Pikafood is website that allows users to submit food requests! Recently I’ve picked up a habit of baking, and I’m always looking for more recipes to try. Coincidentally, there are a bunch of people in my class that are foodies and they always love to try the food I make. I thought it would be convenient for my friends to be able to submit some foods they would like to try and see if I would be able to make them, and that is how Pikafood was born. The name Pikafood comes from a pikachu keychain on my backpack that my friends really like.

### Files:
In the project folder, there are 3 folders and 4 files. 
- flask_session (handles session data)
- static (includes the styles.css file)
- templates (includes the HTML files of all the webpages)
- app.py
- project.db
- README.md
- requirements.txt

Starting from the templates:
All webpages except the homepage include a very simple navigation bar on the top to allow the user to return to the homepage.

`addAdmin.html`
A simple page containing a form for which an admin can register new admins. The user is required to fill in a username, password and the admin key. The admin key is changeable (it is now pikafoodAdminHuhu), and should be provided by an admin to prevent everyone from just registering to become an admin.
