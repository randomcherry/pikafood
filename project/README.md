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

`requests`
Contains 7 columns: id, name, food, additional, recipe, anonymous and upvotes.
id is an autoincrementing column that keep tracks of the IDs of each request that is submitted.
name contains the name of the person who submitted the form so we know who wanted the food even if they ticked anonymous.
additional contains any additional notes such as allergies.
recipe contains a recipe if the user chose to provide one.
anonymous is a boolean which shows if the user would like their name to be shown on the requests page.
upvotes keep tracks of the upvotes on each recipe, this way we know which food is the most popular.

`admins`
Contains 3 columns: adminID, name, password.
A typical table that contains the information of any registered admin accounts.

`finished`
Contains 8 columns: requestID, name, food, additional, recipe, anonymous, rating and upvotes.
This table is similar to the requests table with a new column, rating. This table is used to store finished requests and is viewed on the view finished page, where users can see the ratings of finished recipes.

`comments`
Contains 3 columns: commentID, requestID, comment.
This table keeps track of comments given to finished recipes.

### Templates and app.py
All webpages except the homepage include a very simple navigation bar on the top to allow the user to return to the homepage.

`addAdmin.html`

A simple page containing a form for which an admin can register new admins. The user is required to fill in a username, password and the admin key. The admin key is changeable (it is now pikafoodAdminHuhu), and should be provided by an admin to prevent everyone from just registering to become an admin. An error message is returned if no username or password is provided, the admin key is incorrect or there is a duplicate username.

`adminLogin.html`

Another simple page containing a log in form for admins, where provided information is checked against the admins table in `project.db`. The username is first checked if it exists, then the password is checked. An error message is returned if no username or password is provided, the username does not exist or the password does not match.

`debug.html`

Originally this page was used for debugging, which is why it is called debug.html, but later on I decided to use it as an error/warning page as well. It is just a page with a line of text which displays a warning according to what text is received.

`editRequests.html`

This is a page which only admins can access. The requests, finished and comments table are displayed in this page on the right, with two functions 'Remove request' and 'Finish request' on the left. 'Remove requests' removes the entry of the entered ID, which is used when someone submit something inappropriate or irrelevant. 'Finish requests' moves the entry from the requests table to the finished table, marking it as complete and allowing users to rate it and provide comments.

`index.html`

This is the homepage for the website, containing 5 buttons for redirecting the user to the different pages.

`layout.html`

The template for all the HTML pages.

`rateComment.html`

This page contains a form that allows the user to enter the ID of a finished request and give it a rating with a select menu and/or a comment. The rating can be seen in the view finished page, and it is the average of all ratings. An error message is returned if the request ID is invalid or neither a rating nor a comment is given.

`submitRequest.html`

This page contains a form where the user is able to submit requests, which are stored in the requests table. As seen above in the database section, the user provides provides the same information. An error message is returned if their name or food is not entered.

`viewFinished.html`

This page simply shows the table of finished requests along with the average rating of that recipe.

`viewRequests.html`

This page shows the table unfinished requests, allowing users to upvote requests that they would like to try as well. An error message is returned if the user tries to upvote the same request more than once.
