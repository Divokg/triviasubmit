import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        DB_HOST = os.getenv('DB_HOST','127.0.0.1:5432')
        DB_USER = os.getenv('DB_USER','postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD','123')
        DB_NAME = os.getenv('DB_NAME','trivia_test')
        
        DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = DB_PATH
        setup_db(self.app, self.database_path)
        
        self.new_question={
            "answer": "Highway",
            "category": 4,
            "difficulty": 7,
            "id": 3,
            "question": "What do cars move on"
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
    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        
    def test_404_sent_requesting_beyond_valid_questions_page(self):
        response = self.client().get('/questions?page=1000', json={'rating':1})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    
        
    
        
    def test_delete_question(self):
        response = self.client().delete('/questions/26')
        data = json.loads(response.data)
        
        question = Question.query.filter(Question.id == 26).one_or_none()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 26)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)
            
        
    def test_422_sent_if_question_does_not_exist(self):
        response = self.client().delete('/questions/1000')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    def test_create_new_question(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
        
    def test_405_sent_if_question_creation_not_allowed(self):
        response = self.client().post('/questions/45', json=self.new_question)
        data= json.loads(response.data)
        
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
        
    def test_get_question_search_with_results(self):
        response = self.client().post('/questions', json={'search': 'Which'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 7)
        
    def test_get_question_search_without_results(self):
        response = self.client().post('/questions', json={'search': 'gjgkgsxdfth'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()