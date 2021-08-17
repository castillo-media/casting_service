# Casting Agency

This is an API created for a casting agency. It allows to get and modify data regarding movies and actors. This project has been deployed in Heroku: https://castillomediaheroku.herokuapp.com/.

The Auth0 login URL is: https://castillomedia2.eu.auth0.com/authorize?audience=agency_api&response_type=token&client_id=boSLfn2H452awC7iiuifzxnZeDJ77PHp&
redirect_uri=http://localhost:5000

The different endpoints require authentication in Auth, there are data and actions restrictions based on the role of the authenticated user. There are 3 different roles: casting-assistant, casting-director and executive producer:


## Roles:
-----
### Casting Assistant:
* Can view actors and movies

### Casting Director:
* All permissions a Casting Assistant has and…
* Add or delete an actor from the database
* Modify actors or movies

### Executive Producer:
* All permissions a Casting Director has and…
* Add or delete a movie from the database


## Endpoints:
-----

* <kbd>GET 'api_url/movies'</kbd>   *___(can be accessed by assistant, director and producer)*
* <kbd>POST 'api_url/movies'</kbd>   *____(can be accessed by producer)*
* <kbd>PATCH  'api_url/movies/{movie_id}/edit'</kbd>   *____(can be accessed by director and producer)*
* <kbd>DELETE  'api_url/movies/{movie_id}'</kbd>   *____(can be accessed producer)*
* <kbd>GET 'api_url/people'</kbd>   *____(can be accessed by assistant, director and producer)*
* <kbd>POST 'api_url/people'</kbd>   *____(can be accessed by director and producer)*
* <kbd>PATCH  'api_url/people/{person_id}/edit'</kbd>   *____(can be accessed by director and producer)*
* <kbd>DELETE 'api_url//people/{person_id}'</kbd>   *____(can be accessed by director and producer)*


## Local development
-----

After cloning the repository it would be recommended to work on a virtual environment:
<kbd>python3 -m venv venv/</kbd><br/>
<kbd>source venv/bin/activate</kbd> 

In order to use environment variables run:
<kbd>bash ./setup.sh</kbd> 

Then you need to install the requirements from the starter folder with the following command:
<kbd>pip install -r requirements.txt</kbd>

You must have postgres installed https://www.postgresql.org/ and create two databases, one for development and one for testing (In the code named "agency" and "agency_test" respectively). Then you need to start the database server (See https://www.postgresql.org/docs/13/server-start.html)

Since this project is using Flask, the Flask App must be run with the commands:
<kbd>export FLASK_APP=app</kbd><br/>
<kbd>flask run --reload</kbd><br/>


## Authentication in Auth0
-----

In order to give access to the described endpoints, the api user will be required to go through a sign in process. Depending on the permissions the user is assigned, access to the requested endpoint data will be allowed or denied.

To setup the authentication URL, roles and permissions and to manage registered users the services of Auth0 will be used. If you don´t have one already, you need to create an Auth0 account https://auth0.com/ and do the corresponding setup for three types of roles (Casting Assistant, Casting Director and Executive Producer) and their permissions, the AUTH0_DOMAIN, ALGORITHMS and API_AUDIENCE (These last three in caps are to be found in the setup.sh file for local development, and must be also added as environment variables in Heroku to be used in the deployed application)



## Deployment to Heroku
-----

You will need to create an account with Heroku https://signup.heroku.com/ and then download the Heroku CLI in order to run commands from the terminal that enable us to create a Heroku application and manage it. After you create your account, install Heroku with Homebrew by running:
<kbd>brew tap heroku/brew && brew install heroku</kbd>

After you are done you can verify if it got installed with the command:
<kbd>which heroku</kbd>

If it shows you Heroku is installed, then you can log in with the command:
<kbd>heroku login</kbd>

You will need to create an App in Heroku, to do so run:
<kbd>heroku create name_of_your_app</kbd>

The output will contain a git url for your newly created Heroku application (you will need this url in the command below). You can also go to Heroku Dashboard on the browser to see the newly created application, but it will off course be empty since no code has been pushed to it. You will need to add Heroku to your local repository with the command:
$ git remote add heroku heroku_git_url

Heroku has an addon for apps for a postgresql database instance (The free version "hobby-dev" will be enough for this app). Run this code in order to create your database and connect it to your application:
$ heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application

You will be using some environment variables in Heroku, the just created database and the app URL are already stored in Heroku (upon creation), you can see them with the command:
$ heroku config --app name_of_your_application 

Additionally you will need to add some more environment variable in Heroku to contain the AUTH0_DOMAIN, ALGORITHMS, and API_AUDIENCE. You can do that on the browser from the Dashboard section of your app in Heroku.

(Please keep in mind that for local development the environment variables are stored in the file named setup.sh, but they will be replaced after deployment in Heroku for the ones stored by Heroku)

To push the code to Heroku:
<kbd>git push heroku main</kbd>

Once the app is deployed, run the migrations with:
<kbd>heroku run python manage.py db upgrade --app name_of_your_application</kbd>


## Migrations on Heroku
-----

Heroku can run all your migrations to the database you have hosted on the platform, this will be done by the file named manage.py. 

To mirror how Heroku will run migrations behind the scenes when you deploy the application run the following commands:

<kbd>python manage.py db init</kbd><br/>
<kbd>python manage.py db migrate</kbd><br/>
<kbd>python manage.py db upgrade</kbd><br/>



## Running tests in local development
-----

The endpoints can be tested during local development to make sure they are working properly. To do that use the following commands in these order:

<kbd>dropdb agency_test</kbd><br/>
<kbd>createdb agency_test</kbd><br/>
<kbd>python test_endpoints.py</kbd><br/>


## Code Formatting according to PEP 8 Style
-----

* Install Package: https://pypi.org/project/pycodestyle/ 
* Check File to see if code formatting is correct: <kbd>pycodestyle --first app.py</kbd>



