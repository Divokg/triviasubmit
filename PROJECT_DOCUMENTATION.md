## Udacitrivia 

This is a project that shows both my API and API documentation skills to build a trivia API.


# Getting Started
Developers using this project should already have python3, pip and node installed on their local machines.


# Backend

Run pip install requirements.txt from the backend folder. All erequired packages are included in the requirements file.

Run the following commands:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

These commands put the application in development and directs your application to use the __init__.py file in your flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.

By default the application is run on http://127.0.0.1:5000/ which is a proxy in the frontend configuration.

## Frontend

Run the following commands from the frontend folder.

npm install // only once to install dependencies
npm start 

The frontend will run on localhost:3000.

# Tests

To run tests move to the backend folder and run the following commands:

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

When you run this commands for the first time omit the dropdb command.



# API Reference

# Getting Started
--Authentication: This version of the application does not require API Keys or authentication
--Base URL: This app can only run locally and is not hosted as a base URL.
The backend app is hosted at http://127.0.0.1:5000/, this is set as a proxy in the frontend configuration 

# Error Handling

Errors are returned as JSON objects in the following format:

{
    "success": False,
    "error": 404,
    "message": "resource not found"   
}

The API will return four error types when requests fail:
 404: Resource Not Found
 400: Bad Request
 422: Not Processable
 405: Method not allowed
 500: Server error


 ## Endpoints

 # GET /questions

 --General:
 Returns a list of category objects, a list of question objects, success value and total number of questions.
 Results are paginated in groups of 10. Also include a request argument to choose page number, starting from 1.
 Sample: curl http://127.0.0.1:5000/questions

 {
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"questions": [
{
"answer": "Apollo 13",
"category": 5,
"difficulty": 4,
"id": 2,
"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
},
{
"answer": "Tom Cruise",
"category": 5,
"difficulty": 4,
"id": 4,
"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
},
{
"answer": "Edward Scissorhands",
"category": 5,
"difficulty": 3,
"id": 6,
"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
},
{
"answer": "Muhammad Ali",
"category": 4,
"difficulty": 1,
"id": 9,
"question": "What boxer's original name is Cassius Clay?"
},
{
"answer": "Brazil",
"category": 6,
"difficulty": 3,
"id": 10,
"question": "Which is the only team to play in every soccer World Cup tournament?"
},
{
"answer": "Uruguay",
"category": 6,
"difficulty": 4,
"id": 11,
"question": "Which country won the first ever soccer World Cup in 1930?"
},
{
"answer": "George Washington Carver",
"category": 4,
"difficulty": 2,
"id": 12,
"question": "Who invented Peanut Butter?"
},
{
"answer": "Lake Victoria",
"category": 3,
"difficulty": 2,
"id": 13,
"question": "What is the largest lake in Africa?"
},
{
"answer": "The Palace of Versailles",
"category": 3,
"difficulty": 3,
"id": 14,
"question": "In which royal palace would you find the Hall of Mirrors?"
},
{
"answer": "Agra",
"category": 3,
"difficulty": 2,
"id": 15,
"question": "The Taj Mahal is located in which Indian city?"
}
],
"success": true,
"total_questions": 31
}


# POST /questions
--General:
Creates a new question using the submitted question, answer, difficulty and category. 

Sample: curl http://127.0.0.1:5000/add_question -X POST -H "Content-Type: application/json" -d '{"question":"As black as ?", "answer":"coal", "category":"1", "difficulty":"2"}'

{
  "created": 31,
  "question": {
    "answer": "coal",
    "category": 1,
    "difficulty": 2,
    "id": 31,
    "question": "As black as ?"
  },
  "success": true
}

# GET /categories

General:
Returns a list of category objects, success value and total number of categories.

Sample: curl http://127.0.0.1:5000/categories

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}

# DELETE /questions/{id}

General:
Deletes the question of given {id}. Returns a success value and a list of remaining questions.

Sample: curl -X DELETE http://127.0.0.1:5000/questions/12

{
  "deleted": 12,
  "question deleted": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  },
  "success": true
}

# POST /search

General:
Search for question with the submitted search term. Returns a list of questions that have that search term, success value and total number of questions with that search term.

Sample: curl http://127.0.0.1:5000/search_questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"which"}'

{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Jackson Pollock",
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 7
}

# GET /categories/{id}/questions

General:
Returns a list of questions in the given category per the input ID, success value and total questions of the given category.

Sample: curl http://127.0.0.1:5000/categories/1/questions

{
  "current_category": [
    {
      "id": 1,
      "type": "Science"
    }
  ],
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "pups",
      "category": 1,
      "difficulty": 5,
      "id": 25,
      "question": "What do you call a baby seal"
    },
    {
      "answer": "The Wright Brothers",
      "category": 1,
      "difficulty": 2,
      "id": 38,
      "question": "Who made the first plane"
    },
    {
      "answer": "blue",
      "category": 1,
      "difficulty": 1,
      "id": 42,
      "question": "What is the color of the ocean"
    },
    {
      "answer": "a pod",
      "category": 1,
      "difficulty": 3,
      "id": 43,
      "question": "What do you call a group of dolphins"
    },
    {
      "answer": "a school",
      "category": 1,
      "difficulty": 4,
      "id": 44,
      "question": "What do you call a group of whales"
    },
    {
      "answer": "mercury",
      "category": 1,
      "difficulty": 5,
      "id": 45,
      "question": "What is the nearest planet to the sun?"
    }
  ],
  "success": true,
  "total_questions": 8
}

# POST /play

General: Receives the categorytype and the previous question. Returns the next question in the same type category. 

Sample: curl http://127.0.0.1:5000/play -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"id":"1"}, "previous_questions":[42,26]}'

{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
# Authors

Samuel Ndungu Njoroge

# Acknowledgements

The awesome Tutors and Teachers at Udacity