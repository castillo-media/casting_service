import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Person, Movie


class AgencyTestCase(unittest.TestCase):


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.cast_assist = 'token_value'
        self.cast_director = 'token_value'
        self.exec_prod = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild0YlN4MFNMc090dURsUmhwZElWcyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbGxvbWVkaWEyLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTE5MTEzMWY0Y2U2ODAwNzFkMTgzMTUiLCJhdWQiOiJhZ2VuY3lfYXBpIiwiaWF0IjoxNjI5MTE1NDIyLCJleHAiOjE2MjkxMjI2MjIsImF6cCI6ImJvU0xmbjJINDUyYXdDN2lpdWlmenhuWmVESjc3UEhwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.hGGHV01zNy9_LDFWTtWZRF6VpMPCCcVlT7ELpgVqh3DHTvfdl6exdTIpy-u4WwiQ31BxAHm0vDs0WxrOTkGGPqVR_fkhdg5NOmV-Fw5yBFGFkJBZfKkSdxcMd0kUu00xT26YDtHS7RjtZuszxRr8YD17pVN2WcYm8Gt9bUvgI1g7tJY_aPepq3t2JmUZMkIPWI4TZMQg6FU7RHz1Y3m0iCP74xrQK_E-BDRaixBEmhe7C20EySy4KX0YY7HR8XPkK_NFsgiXNLjKIJ6ke6pq7s7TChH2886x9MlSzXj6c0uKTH2i_N8yAyAdHBf_cakVykzTIflGXsziqgrpDRI9Cw'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass



    def test_get_movies(self):
        res = self.client().get('/movies',
                            headers={'Authorization':
                                     'Bearer ' +self.exec_prod})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_movies_error_wrongURL(self):
        res = self.client().patch('/moviescx',
                            headers={'Authorization':
                                     'Bearer ' +self.exec_prod},
                            json={'name': 'American Beauty',
                                    'release': "2002-04-28"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



    def test_get_actors(self):
        res = self.client().get('/people',
                            headers={'Authorization':
                                        'Bearer ' +self.exec_prod})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_actors_error_methodNotAllowed(self):
        res = self.client().put('/people',
                            headers={'Authorization':
                                        'Bearer ' +self.exec_prod})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')



    def test_post_actor(self):
        res = self.client().post('/people',
                            headers={'Authorization':
                                        'Bearer ' +self.exec_prod},
                            json={"name": "Lola Roteshaus",
                                    "catchphrase": "Early bird catches the worm"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['person']['name'],'Lola Roteshaus')


    def test_post_actor_methodNotAllowed(self):
        res = self.client().patch('/people',
                            headers={'Authorization':
                                        'Bearer ' +self.exec_prod},
                            json={"name": "Lola Roteshaus",
                                    "catchphrase": "Early bird catches the worm"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')



    def test_post_movie(self):
        res = self.client().post('/movies',
                            headers={'Authorization':
                                        'Bearer ' +self.exec_prod},
                            json={'name': 'Night of the living dead',
                                    'release': "1960-10-18"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie']['name'],'Night of the living dead')


    def test_post_movie_wrongURL(self):
        res = self.client().post('/movies/add',
                            headers={'Authorization':
                                        'Bearer ' +self.exec_prod},
                            json={'name': 'Night of the living dead',
                                    'release': "1960-10-18"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')




    def test_patch_actor(self):
        actor_toBe_patched_id=str(1)
        res = self.client().patch('/people/'+actor_toBe_patched_id+'/edit',
                            headers={'Authorization': 'Bearer ' +self.exec_prod},
                            json={"name": "Lola Smith", "catchphrase": "Early bird catches the worm"})
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['person']['name'],'Lola Smith')


    def test_patch_actor_errorIDNotExistent(self):
        actor_toBe_patched_id=str(450)
        res = self.client().patch('/people/'+actor_toBe_patched_id+'/edit',
                            headers={'Authorization': 'Bearer ' +self.exec_prod},
                            json={"name": "Lola Smith", "catchphrase": "Early bird catches the worm"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'internal server error')




    # def test_patch_movie(self):
    #     movie_toBe_patched_id=str(1)
    #     res = self.client().patch('/movies/'+movie_toBe_patched_id+'/edit',
    #                         headers={'Authorization':
    #                                     'Bearer ' +self.exec_prod},
    #                         json={'name': 'Night of the dead',
    #                                 'release': "1960-10-18"})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['movie']['name'],'Night of the dead')


    def test_patch_movie_error(self):
        movie_toBe_patched_id=str(450)
        res = self.client().patch('/movies/'+movie_toBe_patched_id+'/edit',
                            headers={'Authorization':
                                        'Bearer ' +self.exec_prod},
                            json={'name': 'Night of the dead',
                                    'release': "1960-10-18"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)



    def test_delete_actor(self):
        ## Here the actor added in the previous test will be deleted
        actor_toBe_deleted_id=1
        deletion_res = self.client().delete('/people/'+str(actor_toBe_deleted_id),
                        headers={'Authorization':
                                    'Bearer ' +self.exec_prod})
        deletion_data = json.loads(deletion_res.data)

        self.assertEqual(deletion_res.status_code, 200)
        self.assertEqual(deletion_data['success'], True)
        self.assertEqual(deletion_data['deleted_id'], actor_toBe_deleted_id)


    def test_delete_actor_authError(self):
        ## Here the actor added in the previous test will be deleted
        actor_toBe_deleted_id=1
        deletion_res = self.client().delete('/people/'+str(actor_toBe_deleted_id))
        deletion_data = json.loads(deletion_res.data)

        self.assertEqual(deletion_res.status_code, 500)
        self.assertEqual(deletion_data['success'], False)


    def test_delete_movie(self):
        ## Here the movie added in the previous test will be deleted
        movie_toBe_delete_id=1
        deletion_res = self.client().delete('/movies/'+str(movie_toBe_delete_id),
                        headers={'Authorization':
                                    'Bearer ' +self.exec_prod})
        deletion_data = json.loads(deletion_res.data)

        self.assertEqual(deletion_res.status_code, 200)
        self.assertEqual(deletion_data['success'], True)
        self.assertEqual(deletion_data['deleted_id'], movie_toBe_delete_id)


    def test_delete_movie_authError(self):
        ## Here the movie added in the previous test will be deleted
        movie_toBe_delete_id=1
        deletion_res = self.client().delete('/movies/'+str(movie_toBe_delete_id))
        deletion_data = json.loads(deletion_res.data)

        self.assertEqual(deletion_res.status_code, 500)
        self.assertEqual(deletion_data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()