import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import random
from database.models import setup_db, Movie, Actor
from controllers.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  Set up CORS. Allow '*' for origins.
  '''
    CORS(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    #  after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    #  endpoint to get all movies
    @app.route("/movies")
    @requires_auth("get:movies")
    def all_movies(payload):
        try:
            movies = Movie.query.order_by(Movie.id).all()
            return jsonify({
                'success': True,
                "movies": [movie.format() for movie in movies]
            })
        except:
            abort(422)

    # endpoint to get all actors
    @app.route("/actors")
    @requires_auth("get:actors")
    def all_actors(payload):
        actors = Actor.query.order_by(Actor.id).all()
        return jsonify({
            'success': True,
            "actors": [actor.format() for actor in actors],
        })
   # endpoint to delete a movie

    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if (movie is None):
                abort(404)
            else:
                movie.delete()
                return jsonify({
                    "success": True,
                    "deleted_id": id
                })
        except:
            abort(422)

   # endpoint to delete an actor
    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actor(id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if (actor is None):
                abort(404)
            else:
                actor.delete()
                return jsonify({
                    "success": True,
                    "deleted_id": id
                })
        except:
            abort(422)

     # endpoint to add a movie
    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movies")
    def add_movie(payload):
        try:
            body = request.get_json()
            title_requested = body.get("title", None)
            releaseDate_requested = body.get("release_date", None)
            movie = Movie(title=title_requested,
                          release_date=releaseDate_requested)
            movie.insert()
            return jsonify({
                "success": True,
                "movie_created": movie.format()
            })
        except:
            abort(422)
     # endpoint to add a actor

    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actors")
    def add_actor(payload):
        try:
            body = request.get_json()
            name_requested = body.get("name", None)
            age_requested = body.get("age", None)
            gender_requested = body.get("gender", None)
            actor = Actor(name=name_requested, age=age_requested,
                          gender=gender_requested)
            actor.insert()
            return jsonify({
                "success": True,
                "actor_created": actor.format()
            })
        except:
            abort(422)
    # endpoint to update a movie

    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def update_movie(id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)
        try:
            body = request.get_json()
            title_requested = body.get("title", None)
            releaseDate_requested = body.get("release_date", None)
            movie.title = title_requested
            movie.release_date = releaseDate_requested
            movie.update()
            return jsonify({
                "success": True,
                "updated_movie": movie.format()
            })
        except:
            abort(422)

    # endpoint to update an actor
    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def update_actor(id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)
        try:
            body = request.get_json()
            name_requested = body.get("name", None)
            age_requested = body.get("age", None)
            gender_requested = body.get("gender", None)
            actor.name = name_requested
            actor.age = age_requested
            actor.gender = gender_requested
            actor.update()
            return jsonify({
                "success": True,
                "updated_actor": actor.format()
            })
        except:
            abort(422)

    # errors handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request "
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error['description']
        }), AuthError.status_code
    return app
