# Casting Agency

This is an API created for a casting agency. It allows to get and modify data regarding movies and actors. This project has been deployed in Heroku: https://castillomediaheroku.herokuapp.com/.

The Auth0 login URL is: https://castillomedia2.eu.auth0.com/authorize?audience=agency_api&response_type=token&client_id=boSLfn2H452awC7iiuifzxnZeDJ77PHp&
redirect_uri=http://localhost:5000

The different endpoints require authentication, there are data and actions restrictions based on the role of the authenticated user. There are 3 different roles: casting-assistant, casting-director and executive producer:


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

* GET 'api_url/movies'
* POST 'api_url/movies'
* DELETE  'api_url/movies/{movie_id}'
* PATCH  'api_url/movies/{movie_id}/edit'
* GET 'api_url/people'
* POST 'api_url/people'
* DELETE 'api_url//people/{person_id}'
* PATCH  'api_url/people/{person_id}/edit'


