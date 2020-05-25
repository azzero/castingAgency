import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from .models.models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):
    #This class represents the Casting agency test case

    def setUp(self):
        #Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # set tokens : 
        self.casting_assis="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRhQ2x2d0hMdmZGbjhSMWRXbW44bSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWJhOTdhMGViZGMxZDIyMTY0MTIxMjgiLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNTkwNDE2NTg3LCJleHAiOjE1OTA0MjM3ODcsImF6cCI6IlJNQzJMWFFZeTZMYmlpQk9qNmcwb1dNYTBETGFTOU1VIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.Kwfh_o0IFADqq_GPAwXBpsy9UvKzrW6BXTZmIKWbWPPXBrqCKLvZviStAwANS8cAPcKzWvQPjnU2HC5c7GiV4wRDa6vUKTPUAM6YbsVxiQqj08WyvHfpzXHHoe2bArjev5xjlGlABsR9vmNYSs1zCzliOe3jSeK5T7aSVbZffl9asmUJWRaDS95m99XV0BF01-xe0emA1w8bu4stdbe9TGXZXuJaRkihWZpD1dENDSNewCHDMP0eqWsbf9fjekXAI-iAs_1VGqsfgmq9tmUr7IJyYLvXYFcVzubV8eJjvmlj-m6OiKiFgloSyw0jaTMapUq4mvVEd5rX7GpDw6e7xg"
        self.casting_director="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRhQ2x2d0hMdmZGbjhSMWRXbW44bSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMzkyOTg1NjE0ODYxNTMxNjM0OCIsImF1ZCI6WyJjYXN0aW5nQWdlbmN5IiwiaHR0cHM6Ly9mc25kcy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTkwNDI0Mjk5LCJleHAiOjE1OTA0MzE0OTksImF6cCI6IlJNQzJMWFFZeTZMYmlpQk9qNmcwb1dNYTBETGFTOU1VIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.j28rWAtbFHzlPi-CwafE2zsfPgLfsImR7rLV9nVhUH7ZDIsTfZl81YmkP7uV_A7Xzh8OaGz3zqxWYNIV808Ub43m-ZCXYhwrmicngMwgRNTTdqzRFhjotT7m51tmusQyq7ZkfkGAcsuaV6gknRJcDtJ0zvn_a4kgJy-QA7_3jiMhjIMjQWO2abLT7_nypFQXj6u9zazB_vDtWOYn6oo3TJLzoYZc6M9bdum2ZXTf3X1mdoqjB65Suuk0xaPbYXLU9RhnofW1R34SqnObW-pORJBHR7JTu4sX1ovqMuSg9wmKRWaAjkOIkWd6lc5uhpxeAAGPp5lyQP8BfuYhrt-EXg"
        self.casting_moderator="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRhQ2x2d0hMdmZGbjhSMWRXbW44bSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWIyYWMwYjZiNjliYzBjMTJmYWU0YjIiLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNTkwNDIwNTYwLCJleHAiOjE1OTA0Mjc3NjAsImF6cCI6IlJNQzJMWFFZeTZMYmlpQk9qNmcwb1dNYTBETGFTOU1VIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.k1i_FbxEg-F_IRzW35DoovmRrR19WNaa8ztGuZY9WwKDFmCDVcdHIiKhbJC99Mt0sFuNgNbRwh04a_w1rHi144PkBrcW3NP4Dh4qRvfqDxY64LXoP9HyujsnSl56l7T9GltCh-8G3P7ZJyU8dMpGRodmpk2-3g6Sy9sf1S4BveP_gM5l4OkvpiJtdnV4zpreRe8b02jYcXHKLfYpa5uqEiCbahhxAskHdF4y5s4EdixnDU2u-rWg-Ddjm45WIlc2_Cjz09vY_aMPCCqgupe3lBXqexv35bNnbG_H8G4yzArCQPhZT35sFtn_Sr7OkZAFRqB35ih6c3vcuu1Mno2vpg"
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        #Executed after reach test
        pass

    
    # test getting all movies
    def test_getting_movies(self):
        res = self.client().get('/movies',headers={'Authorization':'Bearer '+self.casting_assis})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_401_requesting_beyond_novies_page(self):
        res=self.client().get("movies")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,401)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Authorization header is expected.')
    # get actors test
    def test_get_paginated_actors(self):
        res=self.client().get("/actors",headers={'Authorization':'Bearer '+self.casting_director})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])
    # wrong page test
    def test_401_authorization_header_missing_actors_page(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected')
    def test_create_new_actor(self):
        res=self.client().post("/actors",json={"name":"aziz","age":"34","gender":"man"} ,headers={'Authorization':'Bearer '+self.casting_director} )
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success",True])
        self.assertTrue(data["actor_added"])
    def test_404_create_new_actor_(self):








    # delete question test
    def test_delete_question(self):
        res=self.client().delete("/questions/24")
        question=Question.query.filter(Question.id==24).one_or_none()
        self.assertEqual(res.status_code,200)
        self.assertEqual(question,None)
    delete wrong question test
    def test_422_delete_unexist_question(self):
        res=self.client().delete("/questions/1")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')
    #Add new question test 
    def test_create_new_question(self):
        res=self.client().post("/questions", json={"question":"question test","answer":"answer test ","difficulty":2,"category_value":"1"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
    #test : create new question not allowed
    def test_405_create_new_question_not_allowed(self):
        res=self.client().post("questions/12",json={"question":"question test","answer":"answer test ","difficulty":2,"category_value":"1"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"method not allowed")
    #test : search for question
    def test_search_for_question(self):
        res=self.client().post("/questions/search", json={"searchTerm":"a"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
    # test : searching not found 
    def test_404_searchig_not_found(self):
        res=self.client().post("questions/search/12",json={"searchTerm":"a"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"resource not found")
    # test : get questions by category 
    def test_get_questions_by_category(self):
        res=self.client().get("/categories/1/questions")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
    #test : get questions by categories not found 
    def test_404_get_questions_by_category_not_found(self):
        res=self.client().get("/categories/1/questions/221")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"resource not found")
    #test : quizzes 
    def test_quezzies(self):
        res=self.client().post("/quizzes",json={"previous_questions":[],"quiz_category":{"id":"2","type":"Art"}})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["question"])
    # test : quizzes method not allowed 
    def test_405_quezzes_method_not_allowed(self):
        res=self.client().patch("/quizzes")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"method not allowed")
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()