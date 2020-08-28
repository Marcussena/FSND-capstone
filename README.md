# FSND-capstone
Capstone Project Udacity

Heroku address: https://myagencyapp.herokuapp.com/

Local address: http://127.0.0.1:5000/

Auth0 information for endpoints that require authentication can be found in `setup.sh`.

# Intro

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

- Roles:


- Casting Assistant

	- Can view actors and movies
- Casting Director

	- All permissions a Casting Assistant has and…
	- Add or delete an actor from the database
	- Modify actors or movies
- Executive Producer
	- All permissions a Casting Director has and…
	- Add or delete a movie from the database


# Running tests

To run the unittests, restore a database using the agency_test.psql file provided. From the project folder in terminal run:
```
psql agency > agency_test.
python tests.py
```

# ENDPOINTS
`GET '/'`

- Shows a simple message to test if the environment is running properly:
	
	
	```
	{"Ok":"It is running"}
	
	```


GET '/actors'
- Shows the list of actors in the database:
```
{
    "actors": [
        {
            "actor_age": 61,
            "actor_gender": "Male",
            "actor_name": "Kevin Spacey",
            "id": 2
        },
        {
            "actor_age": 53,
            "actor_gender": "male",
            "actor_name": "Adam Sandler",
            "id": 4
        },
        {
            "actor_age": 62,
            "actor_gender": "female",
            "actor_name": "Meryl Streep",
            "id": 5
        },
        {
            "actor_age": 90,
            "actor_gender": "female",
            "actor_name": "Fernanda Montenegro",
            "id": 6
        },
        {
            "actor_age": 34,
            "actor_gender": "female",
            "actor_name": "Fernanda Paes Leme",
            "id": 7
        }
    ],
    "success": true
}
```
GET '/movies'
- Shows a list of movies in the database.
- Request Arguments: None
- Returns: An object with a single key, movies, that contains multiple objects with a series of string key pairs.
```
{
    "movies": [
        {
            "movie": "King Speech",
            "release_date": "07/18/2019"
        },
        {
            "movie": "Lion King",
            "release_date": "07/18/2019"
        },
        {
            "movie": "Lion King",
            "release_date": "07/18/2019"
        }
    ],
    "success": true
}
```
POST '/actors'
- Posts a new actor to the database, including the name, age and gender
- Returns: A list of actors in the database including the new actor added and a message of success.

```
{
    {
            "actor_age": 52,
            "actor_gender": "male",
            "actor_name": "Nick Offerman",
            "id": 8
     }
    "success": true
}
```
POST '/movies'
- Posts a new movie to the database, including the title and release date
- Returns the list of movies in the database including the new movie added and a message of success.

```
{
    {
            "movie": "Lion King",
            "release_date": "07/18/2019"
    }
    "success": true
}
```
PATCH '/actors/<id>'
- Modifies an existing actor in the database.
- Returns a message of success and the id of the actor updated
	
```
{
    "success": true,
    "updated": {
        "actor_age": 54,
        "actor_gender": "male",
        "actor_name": "Nick Offerman",
        "id": 8
}
```
PATCH '/movies/<int:movie_id>'
- Modifies a existing movie in the database.
- Returns a message of success and the id of the movie updated

```
{
    "success": true,
    "updated": {
        "movie": "Finding Nemo",
        "release_date": "11/15/2005"
}
```
DELETE '/actors/<id>'
- Deletes an actor in the database via the DELETE method and using the actor id.
- Returns the id of the deleted actor and a message of success.
	
```
{
	'id': 5,
	'success': true
}
```
DELETE '/movies/<id>'
- Deletes an actor in the database via the DELETE method and using the movie id.
- Returns the id of the deleted actor and a message of success.
	
```
{
	'id': 5,
	'success': true
}
```


# ERROR HANDLING

The API will return the following errors based on how the request fails:

- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 405: Method Not Allowed
- 422: Unprocessable Entity

# REFERENCES

- I consulted the following websites as reference:

	- https://www.postgresqltutorial.com/postgresql-backup-database/ Postgres backup
	- https://docs.sqlalchemy.org/en/13/errors.html#error-e3q8 SQLAlchemy Error messages
	- https://devcenter.heroku.com/articles/git Heroku deploying with git
	- https://trstringer.com/logging-flask-gunicorn-the-manageable-way/ Solving problems with gunicorn
	
- I also have consulted the following github projects for insight and troubleshooting:

	- https://github.com/the-geekiest-nerd/FSND-Capstone Idea for how to parse authorization headers when testing
	- https://github.com/varlese/FSND-capstone This project helped me to solve some problems I had with errorhandling
	- https://github.com/HyunlangBan/udacity_heroku_sample The sample showed in this project helped me to solve an error when deploying with heroku
