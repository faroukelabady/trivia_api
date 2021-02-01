import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}" \
            .format(
                'postgres',
                'postgres',
                'localhost:5432',
                self.database_name
            )
        self.app = create_app({'database_path': self.database_path})
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)
        self.new_question = {
            'question': 'can you insert into database?',
            'answer': 'Yes, Yes I can.',
            'difficulty': 5,
            'category': 1
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
    DONE
    Write at least one test for each test
    for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])

    def test_404_invalid_questions_page(self):
        res = self.client().get('/api/questions?page=2000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')

    def test_delete_question(self):
        question = Question('test Question', 'test Answer', 1, 4)
        question.insert()
        res = self.client().delete('/api/questions/{}'.format(question.id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_question_delete_does_not_exist(self):
        res = self.client().delete('/api/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_create_new_question(self):
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_question'])
        pass

    def test_422_if_question_create_fails(self):
        res = self.client().post('/api/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        pass

    def test_search_question_with_results(self):
        res = self.client().post('/api/questions/search', json={
            'searchTerm': 'How many'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 1)

    def test_get_book_search_without_results(self):
        res = self.client().post('/api/questions/search', json={
            'search': 'ggggggg'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    def test_get_questions_by_categories(self):
        res = self.client().get('/api/categories/3/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 3)
        self.assertEqual(len(data['questions']), 3)

    def test_quiz_with_result(self):
        res = self.client().post('/api/quizzes', json={
            'previous_questions': [2, 4],
            'quiz_category': {'type': 'Entertainment', 'id': '5'}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['answer'], 'Edward Scissorhands')

    def test_quiz_with_no_result(self):
        res = self.client().post('/api/quizzes', json={
            'previous_questions': [2, 4, 6],
            'quiz_category': {'type': 'Entertainment', 'id': '5'}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['question'])

    def test_422_quiz_with_invalid_data(self):
        res = self.client().post('/api/quizzes', json={
            'previous_questions': [2, 4, 6],
            'quiz_category': {'type': 'Entertainment', 'id': '7'}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
