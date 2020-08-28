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
	
Endpoints
`GET '/actors'`
`GET '/movies'`
`POST '/add-actor'`
`POST '/add-movie'`
`PATCH '/actors/<int:actor_id>'`
`PATCH '/movies/<int:movie_id>'`
`DELETE '/actors/<int:actor_id>'`
`DELETE '/movies/<int:movie_id>'`

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
POST '/actor'
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
POST 'movie'
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
PATCH '/actors/<int:actor_id>'
- Patches an existing actor in the database.
- Request arguments: Actor ID, included as a parameter following a forward slash (/), and the key to be updated passed into the body as a JSON object. For example, to update the age for '/actors/6'
```
{
	"age": "36"
}
```
- Returns: An actor object with the full body of the specified actor ID.
```
{
    "actor": {
        "age": "36",
        "gender": "male",
        "id": 6,
        "name": "Henry Cavill"
    },
    "success": true
}
```
PATCH '/movies/<int:movie_id>'
- Patches an existing movie in the database.
- Request arguments: Movie ID, included as a parameter following a forward slash (/), and the key to be updated, passed into the body as a JSON object. For example, to update the age for '/movies/5'
```
{
	"release": "November 3, 2017"
}
```
- Returns: A movie object with the full body of the specified movie ID.
```
{
    "movie": {
        "id": 5,
        "release": "November 3, 2017",
        "title": "Thor: Ragnarok"
    },
    "success": true
}
```
DELETE '/actors/<int:actor_id>'
- Deletes an actor in the database via the DELETE method and using the actor id.
- Request argument: Actor id, included as a parameter following a forward slash (/).
- Returns: ID for the deleted question and status code of the request.
```
{
	'id': 5,
	'success': true
}
```
DELETE '/movies/<int:movie_id>'
- Deletes a movie in the database via the DELETE method and using the movie id.
- Request argument: Movie id, included as a parameter following a forward slash (/).
- Returns: ID for the deleted question and status code of the request.
```
{
	'id': 5,
	'success': true
}
```
