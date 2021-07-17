import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # Create and configure the app.
    app = Flask(__name__)
    setup_db(app)
    app.secret_key = os.environ.get('SECRET_KEY')

    '''
    Set up CORS.
    '''
    CORS(app)

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    Endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {
                category.id: category.type for category in categories
            },
            'total_categories': len(categories)
        })

    '''
    Endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    '''
    @app.route('/questions')
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.order_by(Category.type).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {
                category.id: category.type for category in categories
            },
            'current_category': None
        })

    '''
    Endpoint to DELETE question using a question ID.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(selection)
            })

        except Exception as err:
            print(err)
            abort(422)

    '''
    Endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(question=new_question,
                                answer=new_answer,
                                category=new_category,
                                difficulty=new_difficulty)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(selection)
            })
        except Exception as err:
            print(err)
            abort(405)

    '''
    POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', '')

        search_results = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()

        current_questions = [question.format() for question in search_results]

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'currentCategory': None,  # can be different categories
        })

    '''
    Endpoint to get questions based on category.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_questions_by_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        current_questions = [question.format() for question in questions]

        category = Category.query.get(category_id)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'currentCategory': category.type,
        })

    '''
    POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    '''
    @app.route('/quizzes', methods=['POST'])
    def create_quiz():
        body = request.get_json()

        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        # Filter questions by category or get all questions.
        # quiz_category['type'] == 'click' - when `All` is selected
        filtered_questions = Question.query.all(
        ) if quiz_category['type'] == 'click' else Question.query.filter_by(
            category=quiz_category['id']).all()
        current_questions = [question.format()
                             for question in filtered_questions]

        if len(current_questions) == 0:
            abort(404)

        next_ids = []

        for question in current_questions:
            if question['id'] not in previous_questions:
                next_ids.append(question['id'])

        # Randomly select a new question.
        random_num = 0 if len(next_ids) == 0 else random.randint(
            0, len(next_ids) - 1)
        question = Question.query.get(next_ids[random_num])

        if not question:
            abort(404)

        current_question = question.format()

        return jsonify({
            'success': True,
            'question': current_question,
            'total_questions': len(current_questions)
        })

    '''
    Error handlers for all expected errors.
    '''
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 404

    @app.errorhandler(405)
    def invalid_method_error(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Invalid Method"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error"
        }), 500

    return app
