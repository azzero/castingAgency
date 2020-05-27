import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):
    # This class represents the Casting agency test case

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # set tokens :
        self.casting_assis = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRhQ2x2d0hMdmZGbjhSMWRXbW44bSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWJhOTdhMGViZGMxZDIyMTY0MTIxMjgiLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNTkwNTA2NDMxLCJleHAiOjE1OTA1OTI4MzEsImF6cCI6IlJNQzJMWFFZeTZMYmlpQk9qNmcwb1dNYTBETGFTOU1VIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.oLaWdp-dfIdPR27XNF73Kgfk3LVpWF7--vFe5y_1oOp3CZazSj7xkH3kmlg3J6AAX2ZaCvEhhjObJfFFeuNEFZughOannCsQJMEJKtEPS67j2ycBZl4BpVO_plw6zM9XfCs1v4v65P7mkMn09BzqwM2BtMxJOQm-4QR5tGeIWxWKATYpRYWsIecXTt2_oH7qvA0XV2ocyPINNc2xWkEMiJC9w6X__bFJG5hqhQPXnQcZU1ARdxV4Nxt-G5o_nIGOnNY6wsiAEaE76HXuscFDLvjq_J37Xi-65evfoRDasi2RdIaQ2Ukwym3TgIpvrqp1RR3embHlBiyGbDQVU9YcsQ"
        self.casting_director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRhQ2x2d0hMdmZGbjhSMWRXbW44bSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMzkyOTg1NjE0ODYxNTMxNjM0OCIsImF1ZCI6WyJjYXN0aW5nQWdlbmN5IiwiaHR0cHM6Ly9mc25kcy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTkwNTA2MjAwLCJleHAiOjE1OTA1OTI2MDAsImF6cCI6IlJNQzJMWFFZeTZMYmlpQk9qNmcwb1dNYTBETGFTOU1VIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.MXimUqg6lst0icxxT6Sr8C5hpDKal7Q51brhrDVF0od7GS8QIMxUf8_KebXBTV4lndo5dWyv78HKPSkuwVQeqTvGIsQurqL4JaNBtNbiTXWu-KgqsTrWkBJBPmkqTPvaT_zYR1sjvaOZ8KhZr0r3cvYNzyulmVIQsnNo6MxH0mY5XnNv7EqDItK-tnR-OD-04D0ZFhbp6VYw7Ol6FM6xCDvu9zrtRy3OyySsdJZ5i-jLyk66sToK6hhcFBBG48Fc5jA05M60k_POrIeCLNvviYxO8O_He2jQQEwyk_wyt2ZrDV9YXCC-bwm6P1HP7M83tYh0wgISbbqOnelRw3yGkA"
        self.casting_moderator = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRhQ2x2d0hMdmZGbjhSMWRXbW44bSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWIyYWMwYjZiNjliYzBjMTJmYWU0YjIiLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNTkwNTA2MzE4LCJleHAiOjE1OTA1OTI3MTgsImF6cCI6IlJNQzJMWFFZeTZMYmlpQk9qNmcwb1dNYTBETGFTOU1VIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.H1LCkVIk28NosAsyTur2iEfkBVOePx1SbDx9eEPPFiepSa-F-LVm8vG6EuV2yOwErSUYtbrerQltlqWJdeL2_QN9SKPuTTAc7mT0B4G-LxObECipq64hbGLUYEKZjXPTyw7W2bXVNmadQTqLyMQns4ujhiK2SNXGRmCsFZeA_r9hWrwAS1Czu5BeNVSQESWj3WQkTOv7ynrDC658zeU-mC-l6ZmB4w59iEjMpWKG3VKVVnw04SRb9RGG7qfz_15BTDet8COmtDDF1zgTePKQm0PRohUsc41XROq13_7c4081pWpU4WTRhE9sWZPwjcux_qJ_OlVfUyD4uhAjR1IZuA"
               # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        # Executed after reach test
        pass


    def insertion():
       movie=Movie(id=1,title='test1',release_date='01/01/2010')
       movie.insert()
       actor=Actor(id=1,name='azedine',age='23',gender='man')
       actor.insert()
       movie=Movie(id=2,title='test2',release_date='02/02/2010')
       movie.insert()
       actor=Actor(id=2,name='aziz',age='34',gender='female')
       actor.insert()

    # POST : 
    # Create Actor :
    # success behavior
    def test_create_new_actor(self):
        res=self.client().post("/actors",json={"name":"aziz","age":"34","gender":"man"} ,headers={'Authorization':'Bearer '+self.casting_director} )
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["actor_created"])
    # error behavior
    def test_405_create_new_actor_with_id_argument(self):
        res=self.client().post("/actors/1",json={"name":"aziz","age":"34","gender":"man"} ,headers={'Authorization':'Bearer '+self.casting_director} )
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data["success"],False)
        self.assertEqual(data['message'],'method not allowed')
    # Create Movie : 
    # success behavior 
    def test_create_new_movie(self):
        res=self.client().post("/movies",json={"title":"romana", "release_date":"09/09/2018"},headers={'Authorization':'Bearer '+self.casting_moderator})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["movie_created"])
    # error behavior 
    def test_405_create_new_movie_with_id_argument(self):
        res=self.client().post("/movies/1",json={"title":"romana", "release_date":"09/09/2018"},headers={'Authorization':'Bearer '+self.casting_moderator})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data["success"],False)
        self.assertEqual(data['message'],'method not allowed')
    # GET 
    # success behavior 
    # test getting all movies
    def test_getting_movies(self):
        res = self.client().get(
            '/movies', headers={'Authorization': 'Bearer '+self.casting_assis})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
    #error behavior 
    def test_405_requesting_beyond_movies_page(self):
        res=self.client().get("movies/1",headers={'Authorization':'Bearer '+self.casting_assis})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'method not allowed')
    # get actors  
    # success behavior 
    def test_get_actors(self):
        res=self.client().get("/actors",headers={'Authorization':'Bearer '+self.casting_assis})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    #error behavior 
    def test_405_requesting_beyond_actors_page(self):
        res=self.client().get("/actors/1",headers={'Authorization':'Bearer '+self.casting_assis})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'method not allowed')

    # PATCH ( update movie )
    # success behavior  
    def test_update_movie(self):
        res=self.client().patch("/movies/1",json={"title":"bartal", "release_date":"02/02/2002"},headers={'Authorization':'Bearer '+self.casting_director})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["updated_movie"])
    # error behavior 
    def test_405_update_movie_without_id(self):
        res=self.client().patch("/movies",json={"title":"bartal", "release_date":"02/02/2002"},headers={'Authorization':'Bearer '+self.casting_director})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data["success"],False)
        self.assertEqual(data['message'],'method not allowed')
    #update actor 
    # success behavior 
    def test_update_actor(self):
        res=self.client().patch("/actors/1",json={"name":"brahim", "age":"45","gender":"man"},headers={'Authorization':'Bearer '+self.casting_director})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["updated_actor"])
    # error behavior 
    def test_405_update_actor_without_id(self):
        res=self.client().patch("/actors",json={"title":"bartal", "release_date":"02/02/2002"},headers={'Authorization':'Bearer '+self.casting_director})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data["success"],False)
        self.assertEqual(data['message'],'method not allowed')
    # DELETE Movie
    # success behavior 
    def test_delete_movie(self):
        res=self.client().delete("/movies/2",headers={'Authorization':'Bearer '+self.casting_moderator})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["deleted_id"])
    # error behavior 
    def test_405_delete_movie_without_id(self):
        res=self.client().delete("/movies",headers={'Authorization':'Bearer '+self.casting_moderator})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data["success"],False)
        self.assertEqual(data['message'],'method not allowed')
    #delete actor : 
    # success behavior 
    def test_delete_actor(self):
        res=self.client().delete("/actors/2",headers={'Authorization':'Bearer '+self.casting_director})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["deleted_id"])
    # error behavior 
    def test_405_delete_actor_without_id(self):
        res=self.client().delete("/actors",headers={'Authorization':'Bearer '+self.casting_director})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data["success"],False)
        self.assertEqual(data['message'],'method not allowed')
    

    def test_401_requesting_beyond_movies_page(self):
        res=self.client().get("movies")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,401)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Authorization header is expected.')
    def test_401_authorization_header_missing_actors_page(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')    
    def test_401_Permission_not_found_create_new_actor(self):
        res=self.client().post("/actors",json={"name":"aziz","age":"34","gender":"man"} ,headers={'Authorization':'Bearer '+self.casting_assis} )
        data=json.loads(res.data)
        self.assertEqual(res.status_code,401)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"Permission not found.")
if __name__ == "__main__":
    unittest.main()
