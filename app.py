import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask, request, jsonify, abort
from models import setup_db, Movie, Person
import json
from auth import AuthError, requires_auth, get_token_auth_header, verify_decode_jwt, check_permissions


db = SQLAlchemy()


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,DELETE,OPTIONS')
        return response


    @app.route('/')
    def get_greeting():
        # excited = os.environ['EXCITED']
        greeting = "Hello World" 
        # if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"


    @app.route('/people', methods=['GET'])
    @requires_auth('get:actors')
    def getPeople(self):
        try:
            all_people = db.session.query(Person).all()
            people_list=[]
            for person in all_people:
                person={'id':person.id,'person_name':person.name,'movie_catchphrase':person.catchphrase}
                people_list.append(person)

        except:
            abort(422)
        finally:
            db.session.close()
            return jsonify({
                'success': True,
                'person':people_list
            })




    @app.route('/people', methods=['POST'])
    @requires_auth('post:actor')
    def postPerson(self):
        body = request.get_json()
        new_name = body['name']
        new_catchphrase = body['catchphrase']

        try:
            person = Person(
                name=str(new_name),
                catchphrase=str(new_catchphrase)
            )
            db.session.add(person)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
            return jsonify({
                "success": True,
                "person": body
            })


    @app.route('/people/<int:person_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def deletePerson(self,person_id):
        try:
            person_to_delete = db.session.query(Person).filter(Person.id == person_id)\
                              .one_or_none()
            db.session.delete(person_to_delete)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()
            return jsonify({
                'success': True,
                'deleted_id': person_id
            })



    @app.route('/people/<int:person_id>/edit', methods=['PATCH'])
    @requires_auth('patch:actor')
    def editPerson(self,person_id):
        body = request.get_json()
        new_name = body['name']
        new_catchphrase = body['catchphrase']
        try:
            personToEdit = Person.query.filter(Person.id == person_id)\
                          .one_or_none()
            personToEdit.name = new_name
            personToEdit.catchphrase = new_catchphrase
            personToEdit.update()
        except Exception:
            db.session.rollback()
            db.session.close()
            abort(422)
        finally:
            db.session.close()
            return jsonify({
                'success': True,
                'person': {
                    "name": personToEdit.name,
                    "catchphrase": personToEdit.catchphrase
                }
            })



    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def getMovies(self):
        try:
            all_movies = db.session.query(Movie).all()
            movies_list=[]
            for movie in all_movies:
                movie_unit={'id':movie.id,'movie_name':movie.name,'movie_release':movie.release}
                movies_list.append(movie_unit)

        except:
            abort(422)
        finally:
            db.session.close()
            return jsonify({
                "success": True,
                'movies':movies_list
            })



    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def postMovie(self):
        body = request.get_json()
        new_name = body['name']
        new_release = body['release']

        try:
            movie = Movie(
                name=str(new_name),
                release=str(new_release)
            )
            db.session.add(movie)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
            return jsonify({
                "success": True,
                "movie": body
            })




    @app.route('/movies/<int:movie_id>/edit', methods=['PATCH'])
    @requires_auth('patch:movie')
    def editMovie(self,movie_id):
        body = request.get_json()
        new_name = body['name']
        new_release = body['release']
        error=False
        try:
            movieToEdit = Movie.query.filter(Movie.id == movie_id)\
                .one_or_none()
            movieToEdit.name = new_name
            movieToEdit.release = new_release
        except Exception:
            db.session.rollback()
            db.session.close()
            error=True
            abort(422)
        finally:
            if not error:
                movieToEdit.update()              
                db.session.close()
                return jsonify({
                    'success': True,
                    'movie': {
                        "name": movieToEdit.name,
                        "release": movieToEdit.release
                    }
                })
            else:
                db.session.rollback()
                db.session.close()
                abort(404)




    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def deleteMovie(self,movie_id):
        try:
            movie_to_delete = db.session.query(Movie).filter(Movie.id == movie_id)\
                              .one_or_none()
            db.session.delete(movie_to_delete)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()
            return jsonify({
                'success': True,
                'deleted_id': movie_id
            })


    @app.errorhandler(401)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401  


    @app.errorhandler(404)
    def resourceNotFound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(405)
    def resourceNotFound(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(500)
    def resourceNotFound(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500



    return app


    @app.errorhandler(AuthError)
    def authorizationError(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response


app = create_app()

if __name__ == '__main__':
    app.run()