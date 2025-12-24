# Pikafood
#### Video Demo: [URL](https://youtu.be/JFwH7OAu0FY)

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

### Database: `project.db`.
The database contains 4 tables that are used:

#### requests
Contains 7 columns: id, name, food, additional, recipe, anonymous and upvotes. 
id is an autoincrementing column that keep tracks of the IDs of each request that is submitted.
name contains the name of the person who submitted the form so we know who wanted the food even if they ticked anonymous.
additional contains any additional notes such as allergies.
recipe contains a recipe if the user chose to provide one.
anonymous is a boolean which shows if the user would like their name to be shown on the requests page.
upvotes keep tracks of the upvotes on each recipe, this way we know which food is the most popular.

#### admins
Contains 3 columns: adminID, name, password.
A typical table that contains the information of any registered admin accounts.

#### finished
Contains 8 columns: requestID, name, food, additional, recipe, anonymous, rating and upvotes.
This table is similar to the requests table with a new column, rating. This table is used to store finished requests and is viewed on the view finished page, where users can see the ratings of finished recipes.

#### comments
Contains 3 columns: commentID, requestID, comment.
This table keeps track of comments given to finished recipes.

### Templates and app.py
All webpages except the homepage include a very simple navigation bar on the top to allow the user to return to the homepage.

`addAdmin.html`

A simple page containing a form for which an admin can register new admins. The user is required to fill in a username, password and the admin key. The admin key is changeable (it is now pikafoodAdminHuhu), and should be provided by an admin to prevent everyone from just registering to become an admin. An error message is returned if no username or password is provided, the admin key is incorrect or there is a duplicate username.

`adminLogin.html`

Another simple page containing a log in form for admins, where provided information is checked against the admins table in `project.db`. The username is first checked if it exists, then the password is checked. An error message is returned if no username or password is provided, the username does not exist or the password does not match.
