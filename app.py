import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth.auth import *

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # command to initialize the tables of the database (uncomment to start the database)
  #db_drop_and_create_all()

  # CORS app configuration
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  # CORS Headers setup
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Headers', 'GET, PATCH, POST, DELETE, OPTIONS')
      return response


  # GET end point to test if it's ok
  @app.route('/', methods=['GET'])
  def ok():
      return jsonify({'Ok':'It is running'}), 200

  @app.route('/actors', methods=['GET'])
  @requires_auth("get:actors")
  def get_actors(payload):
      actors = Actor.query.order_by(Actor.id).all()
      actors_list = [a.summarize() for a in actors]

      return jsonify({
      'success': True,
      'actors': actors_list
      }), 200

  @app.route('/movies', methods=['GET'])
  @requires_auth("get:movies")
  def get_movies(payload):
      movies = Movie.query.order_by(Movie.id).all()
      movies_list = [m.summarize() for m in movies]

      return jsonify({
      'success': True,
      'movies': movies_list
      }), 200

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(token):
      #getting data parsed
      data = request.get_json()

      try:
          #checking if the data contains 'name', 'age' and 'gender'
          if (('name' in data) and ('age' in data) and ('gender' in data)):
              new_actor = Actor(name=data['name'], age=data['age'], gender=data['gender'])
              new_actor.insert()
              actors_list = [a.summarize() for a in Actor.query.all()]

              #return success message
              return jsonify({
                  'success': True,
                  'actors': actors_list
              })
          if (('name' not in data) or ('age' not in data) or ('gender' not in data)):
              raise KeyError
      except KeyError:
          abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(token):
      #getting data parsed
      data = request.get_json()

      try:
          #checking if the data contains 'title' and 'release_date'
          if (('title' in data) and ('release_date' in data)):
              new_movie = Movie(title=data['title'], release_date=data['release_date'])
              new_movie.insert()
              movies_list = [m.summarize() for m in Movie.query.all()]

              #return success message
              return jsonify({
                  'success': True,
                  'movies': movies_list
              })
          else:
              abort(422)
      except BaseException:
          abort(400)

  @app.route('/actors/<id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def edit_actors(token,id):
      #getting token's data
      data = request.get_json()
      #selecting the actor that we want to update
      updated_actor = Actor.query.get(id)

      if not updated_actor:
          abort(404)
      if not id:
          abort(404)

      name = data['name']
      age = data['age']
      gender = data['gender']

      updated_actor.name = name
      updated_actor.age = age
      updated_actor.gender= gender

      updated_actor.update()
      actors_list = [a.summarize() for a in Actor.query.all()]


      return jsonify({
          'success': True,
          'actors': actors_list,
          'updated': updated_actor.summarize()
      })

  @app.route('/movies/<id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def edit_movies(token,id):
      #getting token's data
      data = request.get_json()
      #selecting the movie that we want to update
      updated_movie = Movie.query.get(id)

      if not updated_movie:
          abort(404)
      if not id:
          abort(404)

      title = data['title']
      release_date = data['release_date']

      updated_movie.title = title
      updated_movie.release_date = release_date

      updated_movie.update()
      movies_list = [m.summarize() for m in Movie.query.all()]


      return jsonify({
          'success': True,
          'actors': movies_list,
          'updated': updated_movie.summarize()
      })

  @app.route('/actors/<id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(token,id):
      #selecting the actor that we want to delete
      deleted_actor = Actor.query.get(id)

      if not deleted_actor:
          abort(404)
      try:
          Actor.delete(deleted_actor)
          actors_list = [a.summarize() for a in Actor.query.all()]
          return jsonify({
              'success': True,
              'deleted': id,
              'actors': actors_list
          })
      except BaseException:
          abort(422)

  @app.route('/movies/<id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(token,id):
      #selecting the actor that we want to delete
      deleted_movie = Movie.query.get(id)

      if not deleted_movie:
          abort(404)
      try:
          Movie.delete(deleted_movie)
          movies_list = [m.summarize() for m in Movie.query.all()]
          return jsonify({
              'success': True,
              'deleted': id,
              'actors': movies_list
          })
      except BaseException:
          abort(422)

  ## Error Handling

  @app.errorhandler(401)
  def not_authorized(error):
      return jsonify({
                      "success": False,
                      "error": 401,
                      "message": "Authorization Header is missing"
                      }), 401

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False,
                      "error": 422,
                      "message": "unprocessable"
                      }), 422


  @app.errorhandler(404)
  def resource_not_found(error):
      return jsonify({
                      "success": False,
                      "error": 404,
                      "message": "resource not found"
                      }), 404


  @app.errorhandler(AuthError)
  def authError_handler(e):
      return jsonify({
                      "success": False,
                      "error": e.status_code,
                      "message": e.error
                      }), e.status_code






  return app

APP = create_app()

if __name__ == '__main__':
    APP.run()
