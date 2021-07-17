
# Full Stack Trivia

The application must:
1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Backend

### Installing Dependencies for the Backend
1.  **Python 3.7** - [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
2.  **Virtual Enviornment** - [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
3.  **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

4.  **Key Dependencies**
-  [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
-  [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM to handle the lightweight sqlite database.
-  [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension to handle cross origin requests from our frontend server.

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```
The `--reload` flag will detect file changes and restart the server automatically.

### Tasks

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

### API Endpoints

`GET '/categories'`
- Fetches a dictionary of categories.
- Request arguments: none.
- Returns: an object with a `categories` key in the next format - `{ category_id: category_value }`.
```
{
	'1' : "Science",
	'2' : "Art",
	'3' : "Geography",
	'4' : "History",
	'5' : "Entertainment",
	'6' : "Sports"
}
```

`GET '/questions?page=pageNum>'`
- Fetches a paginated set of questions.
- Request arguments: page - pageNum(int).
- Returns: an object with 10 paginated questions, total questions, object including all categories, and current category string.
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { 
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports" 
        },
    'currentCategory': null
}
```

`GET '/categories/:categoryId/questions'`
- Fetches questions for a cateogry specified by id request argument.
- Request arguments: id - integer.
- Returns: an object with questions for the specified category, total questions, and current category string.
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

`DELETE '/questions/:questionId'`
- Deletes a specified question using the id of the question.
- Request arguments: id - integer.
- Returns: does not need to return anything besides the appropriate HTTP status code.

`POST '/quizzes'`
- Sends a post request in order to get the next question. 
- Request body: 
```
{
    'previous_questions': an array of question ids,
    'quiz_category': a string of the current category 
}
```
- Returns: a single new question object, and a number of total questions.
```
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
    'totalQuestions': 10,
}
```

`POST '/questions'`
- Sends a post request in order to add a new question.
- Request Body:
```
{
    'question': 'A new question string',
    'answer': 'A new answer string',
    'difficulty': 1,
    'category': 3,
}
```
- Returns: does not return any new data.

`POST '/questions/search'`
- Sends a post request in order to search for a specific question by a search term. 
- Request Body:
```
{
    'searchTerm': 'search term'
}
```
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category.
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': null
}
```


### Testing

To run the tests, run

```

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

```

## Frontend

### Installing Dependencies

1. **Installing Node and NPM**<br>
Download and install Node [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**<br>
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
```bash
npm install
```

### Running Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.
