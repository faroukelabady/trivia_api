import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import traceback
from sqlalchemy import inspect, and_

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if test_config is not None:
        setup_db(app, test_config['database_path'])
    else:
        setup_db(app)

    '''
    @DONE: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @DONE: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )
        return response

    '''
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/api/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)
        categories_result = {}
        for category in categories:
            categories_result[category.id] = category.type.lower()
        return jsonify({
          'success': True,
          'categories': categories_result
        })

    '''
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at
    the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/api/questions')
    def get_paginated_questions():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        result = paginate_selection(request, questions, QUESTIONS_PER_PAGE)

        if len(result) == 0:
            abort(404)

        categories_result = {}
        for category in categories:
            categories_result[category.id] = category.type.lower()

        return jsonify({
          'success': True,
          'questions': result,
          'total_questions': len(questions),
          'categories': categories_result
        })

    '''
    @DONE:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id,
            })
        except:
            abort(422)

    '''
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will
    appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/api/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        try:
            new_question = Question(
              question=question,
              answer=answer,
              category=category,
              difficulty=difficulty
            )
            new_question.insert()
            return jsonify({
              'success': True,
              'created_question': new_question.id,
            })
        except:
            abort(422)

    '''
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/api/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search = body.get('searchTerm', None)
        try:
            result = Question.query \
              .filter(Question.question.ilike('%{}%'.format(search))) \
              .order_by(Question.id).all()
            found_questions = paginate_selection(
              request,
              result,
              QUESTIONS_PER_PAGE
            )
            return jsonify({
              'success': True,
              'questions': found_questions,
              'total_questions': len(result),
            })
        except:
            abort(422)

    '''
    @DONE:
    Create a GET endpoint to get questions based on category.
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/api/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        questions = Question.query.order_by(Question.id) \
          .filter(Question.category == category_id).all()
        current_category = Category.query.get(category_id)
        result = paginate_selection(request, questions, QUESTIONS_PER_PAGE)
        if len(result) == 0:
            abort(404)

        category_result = {}
        category_result[current_category.id] = current_category.type.lower()

        return jsonify({
          'success': True,
          'questions': result,
          'total_questions': len(questions),
          'currentCategory': category_result
        })

    '''
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/api/quizzes', methods=['POST'])
    def create_quiz():
        body = request.get_json()
        previousQuestions = body.get('previous_questions', None)
        quizCategory = body.get('quiz_category', None)
        try:
            avaliableQuestions = Question.query \
                .filter(Question.id.notin_(previousQuestions))

            if(int(quizCategory['id']) > 0):
                category = Category.query \
                    .filter(Category.id == int(quizCategory['id'])) \
                    .one_or_none()
                if category is None:
                    abort(404)
                avaliableQuestions = avaliableQuestions \
                    .filter(Question.category == int(quizCategory['id']))

            avaliableQuestions = avaliableQuestions.all()
            result = None
            if(len(avaliableQuestions) > 0):
                result = random.choice([question.format()
                                        for question in avaliableQuestions])

            return jsonify({
              'success': True,
              'question': result
            })
        except:
            traceback.print_exc()
            abort(422)

    '''
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource Not Found"
          }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable Entity"
          }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
          }), 400

    return app


def paginate_selection(request, selection, page_size):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * page_size
    end = start + page_size
    result = [item.format() for item in selection]
    current_selection = result[start:end]
    return current_selection
