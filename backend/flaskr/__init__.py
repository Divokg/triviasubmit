
from operator import truediv
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Paginate questions 10 per page
# Source: https://www.youtube.com/watch?v=jwQhPIaQpgg
def paginate_questions(request, selection):
  page = request.args.get('page',1, type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  
  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app) 
  migrate = Migrate()
  migrate.init_app(app, setup_db)
  
 # Setting up CORS
  cors = CORS(app, resources={r"/api/*" : {"origins":"*"}})
  
 # Home route
  @app.route('/')
  def welcome():
    return jsonify({
      'message': 'insert a request endpoint'
    })
 
 # Setting up Access-Control-Allow
 # https://classroom.udacity.com/nanodegrees/nd0044-alg-t2/parts/cd0037/modules/830942ca-97fe-4f46-8a46-a156b765c1e3/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/dc060384-b508-4a13-839e-01b636105556
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response
  
 # Endpoint to handle GET requests for all available categories.
 # Source: https://www.youtube.com/watch?v=jwQhPIaQpgg
  
  @app.route('/categories')
  def retrieve_categories():
      #retrieve categories from db
      categories = Category.query.order_by(Category.id).all()
      new_categories = {category.id:category.type for category in categories}
      
      return {
      'categories': new_categories
    }

 # Endpoint to handle GET requests for questions 
 # Source: https://www.youtube.com/watch?v=jwQhPIaQpgg
 
  @app.route('/questions', methods = ['GET'])
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    
    if len(current_questions) == 0:
      abort (404)
    
    categories=Category.query.order_by(Category.id).all()
    new_categories = {category.id:category.type for category in categories}
    
    return {
      'success': True,
      'questions': current_questions,
      'categories': new_categories,
      'total_questions': len(Question.query.all())
    }
  
  # Endpoint to get specific question by id
  # Endpoint not needed but nice to have  
  
  @app.route('/questions/<int:question_id>')
  def get_question_by_id(question_id):
    question = Question.query.get_or_404(question_id)
    
    return{
      'question':question.format()
    }  
  
  
  
  # Endpoint to DELETE question using a question ID. 
  # Source https://www.youtube.com/watch?v=P7lkioo-igM
  
  @app.route('/delete/<int:question_id>', methods=['DELETE'])
  def delete(question_id):
    
    try:
      question = Question.query.get_or_404(question_id)
      question.delete()
      
      return {
        'success': True,
        'question deleted': question.format(),
        'deleted': question_id
      }
    
    except:
      abort(422)
    

  # Endpoint to POST a new question,
  # Source: https://www.youtube.com/watch?v=xpo0ooa0U7A 
 
  @app.route('/add_question', methods=['POST'])
  def create_question():
    form = request.get_json()
    question = Question(question=form.get('question'), answer=form.get('answer'), category= form.get('category'), difficulty=form.get('difficulty'))
        
    try:
       question.insert()
       formatted_question = question.format()
      
       return {
        'success': True,
        'created': question.id,
        'question':formatted_question
      }
      
    except:
      abort(422) 



 # Endpoint to get questions based on a search term. 
 # Source: https://docs.sqlalchemy.org/en/14/orm/internals.html?highlight=ilike#sqlalchemy.orm.PropComparator.ilike                                      
 
  @app.route('/search_questions', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search = body.get('searchTerm', None)
   
    try:
      if search:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
        current_questions = paginate_questions(request, selection)
        
        return {
          'success': True,
          'questions': current_questions,
          'total_questions': len(selection.all())
        }
    except:
      abort(404)
        
# Endpoint to get questions based on category. 

  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_per_category(category_id):
    #retrieve the questions
    questions = Question.query.filter(Question.category == category_id)
    selected_questions = paginate_questions(request, questions)
    # retrieve the categories
    categories = Category.query.filter(Category.id == category_id)
    formatted_categories = [category.format() for category in categories]
   
    return {
      'questions' : selected_questions,
      'success': True,
      'total_questions': len(selected_questions),
      'current_category':formatted_categories
    }
     
  # POST endpoint to get questions to play the quiz. 
  # Source: 
    
  @app.route('/play',methods=['POST'])
     
  def quiz_game():
    # Source: https://www.youtube.com/watch?v=xpo0ooa0U7A&t=51s
    play_category = request.get_json().get('quiz_category')
    play_previous = request.get_json().get('previous_questions')
    
    try:
      if int(play_category['id']) == 0:
        questions = Question.query.all()
      else:
        #Source: https://docs.sqlalchemy.org/en/13/core/sqlelement.html?highlight=not_#sqlalchemy.sql.expression.not_
        questions = (
          Question.query.filter(~Question.id.in_(play_previous)).filter(Question.category == int(play_category['id'])).all()    
        )
      play_questions = [question.format() for question in questions]
      #Source: https://www.w3schools.com/python/ref_random_choice.asp
      next_question = (random.choice(play_questions)if play_questions else None)
      return {
        'success': True,
        'question': next_question
      }
    except :
      abort(422)
    
    
 # Error handlers for all expected errors 
 # Source: https://classroom.udacity.com/nanodegrees/nd0044-alg-t2/parts/cd0037/modules/830942ca-97fe-4f46-8a46-a156b765c1e3/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/8755536a-7966-476b-81ac-063db44c85d4
  @app.errorhandler(404)
  def not_found(error):
    return {
      "success": False,
      "error": 404,
      "message": "resource not found"   
    }, 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return {
      "success": False,
      "error": 422,
      "message": "unprocessable"   
    }, 422
    
  @app.errorhandler(400)
  def bad_request(error):
    return {
      "success": False,
      "error": 400,
      "message": "bad request"   
    }, 400
    
  @app.errorhandler(405)
  def method_not_allowed(error):
    return {
      "success": False,
      "error": 405,
      "message": "method not allowed"   
    }, 405
    
  @app.errorhandler(500)
  def server_error(error):
    return {
      "success": False,
      "error": 500,
      "message": "server error"   
    }, 500
  
  return app



    