import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.assistant_token = os.environ['assistant_token']
        self.director_token = os.environ['director_token']
        self.producer_token = os.environ['producer_token']
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = 'postgresql://postgres:postgres@localhost:5432/agency_test'
        setup_db(self.app, self.database_path)

        #sample actor and movie for use in tests#

        self.sample_movie = {
            'title': 'Big Daddy',
            'release_date': '10/08/1999'
        }

        self.sample_actor = {
            'name': 'Leonardo Di Caprio',
            'age': 45,
            'gender': 'male'
        }

        self.sample_invalid_actor = {
            'name' : 'Meryl Streep'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_ok_page(self):
        #test response#
        res = self.client().get('/')
        data = json.loads(res.data)

        #test if the response has all information#
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Ok'], 'It is running')

    def test_get_actors(self):
        #testing if /actors returns a list of actors#
        res = self.client().get('/actors', headers={'Authorization': "Bearer {}".format(self.assistant_token)})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_actors_failed(self):
        #test response for getting the list of actors without authorization#
        res = self.client().get('/actors')
        data = json.loads(res.data)
        # test if the status code is 401 (unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data['message']['description'], 'Authorization Header is missing')

    def test_get_movies(self):
        """Passing Test for GET /movies"""
        res = self.client().get('/movies', headers={'Authorization': "Bearer {}".format(self.assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movies', data)

    def test_get_movies_failed(self):
        #test response for getting the list of movies without authorization#
        res = self.client().get('/movies')
        data = json.loads(res.data)
        # test if the status code is 401 (unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data['message']['description'], 'Authorization Header is missing')

    def test_post_actor(self):
        #test response for successfully posting an actor with the director token
        res = self.client().post('/actors', headers={'Authorization': "Bearer {}".format(self.director_token)}, json=self.sample_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    def test_post_actor_failed(self):
        #test response for posting an invalid actor with the director token
        res = self.client().post('/actors', headers={'Authorization': "Bearer {}".format(self.director_token)}, json=self.sample_invalid_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], 'unprocessable')

    def test_post_actor_401(self):
        #test response for FAILED post request to add an actor with the assistant token
        res = self.client().post('/actors', headers={'Authorization': "Bearer {}".format(self.assistant_token)}, json=self.sample_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data['message']['message'],'Permission not authorized')

    def test_post_movie(self):
        #test response for successfully posting an actor with the Executive Producer token
        res = self.client().post('/movies', headers={'Authorization': "Bearer {}".format(self.producer_token)}, json=self.sample_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        movies = Movie.query.all()
        self.assertEqual(len(data['movies']), len(movies))

    def test_post_movie_failed(self):
        #test response for unsuccessfully posting a movie with the director token (unauthorized)
        res = self.client().post('/movies', headers={'Authorization': "Bearer {}".format(self.director_token)}, json=self.sample_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data['message']['message'], 'Permission not authorized')

    def test_post_movie_401(self):
        #test response for FAILED post request to add a movie with the assistant token
        res = self.client().post('/movies', headers={'Authorization': "Bearer {}".format(self.assistant_token)}, json=self.sample_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data['message']['message'],'Permission not authorized')

    def test_patch_actor(self):
        #test response for modifying actor information using the director_token
        res = self.client().patch('/actors/5', headers={'Authorization': "Bearer {}".format(self.director_token)}, json=self.sample_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["updated"]["actor_name"], self.sample_actor["name"])
        self.assertEqual(data["updated"]["actor_age"], self.sample_actor["age"])
        self.assertEqual(data["updated"]["actor_gender"], self.sample_actor["gender"])

    def test_patch_actor_failed(self):
        #test response for modifying actor not found (404)
        res = self.client().patch('/actors/999', headers={'Authorization': "Bearer {}".format(self.director_token)}, json=self.sample_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_patch_movie(self):
        #test response for modifying movie information using the director_token
        res = self.client().patch('/movies/5', headers={'Authorization': "Bearer {}".format(self.director_token)}, json=self.sample_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["updated"]["movie"], self.sample_movie["title"])
        self.assertEqual(data["updated"]["release_date"], self.sample_movie["release_date"])

    def test_patch_movie_failed(self):
        #test response for modifying movie not found (404)
        res = self.client().patch('/movies/999', headers={'Authorization': "Bearer {}".format(self.director_token)}, json=self.sample_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_actor(self):
        # test response for successfully deleting an actor with the producer token
        res = self.client().delete('/actors/2', headers={'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('deleted', data)

    def test_delete_movie(self):
        # test response for successfully deleting a movie with the producer token
        res = self.client().delete('/movies/2', headers={'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('deleted', data)

    def test_delete_actor_failed(self):
        # test response for deleting an actor that does not exist in the database
        res = self.client().delete('/actors/999', headers={'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    def test_delete_movie_failed(self):
        # test response for deleting a movie that does not exist in the database
        res = self.client().delete('/movies/999', headers={'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    def test_add_actor_failed_401(self):
        # test response for trying add an actor with wrong authorization (director token)
        res = self.client().post('/movies', headers={'Authorization': "Bearer {}".format(self.director_token)}, json=self.sample_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data['message']['message'],'Permission not authorized')

    def test_delete_movie_failed_401(self):
        # test response for trying delete a movie with wrong authorization (director token)
        res = self.client().delete('/movies/3', headers={'Authorization': "Bearer {}".format(self.director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data['message']['message'],'Permission not authorized')





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
