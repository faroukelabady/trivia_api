# API Reference
---
## Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

## GET /api/categories
- **General:**
  - Returns a list of question categories, success value.
- **Sample curl bash request:** ` curl http://127.0.0.1:5000/api/categories `
- **Error:**
    - 404 (if there is no categories) 
- **sample response:**
``` json
{
  "categories": {
    "1": "science", 
    "2": "art", 
    "3": "geography", 
    "4": "history", 
    "5": "entertainment", 
    "6": "sports"
  }, 
  "success": true
}
```

## GET /api/questions
- **General:**
  - Returns a list of questions, success value, categories list, and total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from
- **Sample curl bash request:** ` curl -X GET "http://127.0.0.1:5000/api/questions?page=1" `
- **Error:**
    - 404 (if there is no questions) 
- **sample response:**
``` json
{
  "categories": {
    "1": "science", 
    "2": "art", 
    "3": "geography", 
    "4": "history", 
    "5": "entertainment", 
    "6": "sports"
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
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
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
    }
  ], 
  "success": true, 
  "total_questions": 20
}
```

## POST /api/questions
- **General:**
  - Creates a new question using the submitted values. Returns the id of the created question, success value.
- **Sample curl bash request:** ` curl -X POST http://127.0.0.1:5000/api/questions -H "Content-Type: application/json" -d '{"question":"What is my favorite Food?", "answer":"Mango", "difficulty":"4", "category": "1"}' `
- **Error:**
    - 422 (if question couldn't be created) 
- **sample response:**
``` json
{
  "created_question": 26, 
  "success": true
}
```

## DELETE /api/questions/{question_id}
- **General:**
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value.
- **Sample curl bash request:** ` curl -X DELETE http://127.0.0.1:5000/api/questions/20 `
- **Error:**
    - 422 (if question does not exists) 
- **sample response:**
``` json
{
  "deleted": 20, 
  "success": true
}
```

## POST /api/questions/search
- **General:**
  - Search by question case insenstive. Returns a list of questions, success value, and total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from
- **Sample curl bash request:** ` curl -X POST "http://127.0.0.1:5000/api/questions/search?page=1" -H "Content-Type: application/json" -d '{"searchTerm":"What is my favorite Food?"}' `
- **sample response:**
``` json
{
  "questions": [
    {
      "answer": "Mango", 
      "category": 1, 
      "difficulty": 4, 
      "id": 26, 
      "question": "What is my favorite Food?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```
## GET /api/categories/{category_id}/questions
- **General:**
  - get questions by category id. Returns a list of questions, success value, current category, and total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from
- **Sample curl bash request:** ` curl -X GET "http://127.0.0.1:5000/api/categories/1/questions?page=1" `
- **sample response:**
``` json
{
  "currentCategory": {
    "1": "science"
  }, 
  "questions": [
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "BMW", 
      "category": 1, 
      "difficulty": 3, 
      "id": 25, 
      "question": "coolest caar"
    }, 
    {
      "answer": "Mango", 
      "category": 1, 
      "difficulty": 4, 
      "id": 26, 
      "question": "What is my favorite Food?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```

## POST /api/quizzes
- **General:**
  - get quizz question by category and exclude previous questions id. Returns a random question, and success value.
- **Sample curl bash request:** ` curl -X POST "http://127.0.0.1:5000/api/quizzes" -H "Content-Type: application/json" -d '{"previous_questions":[2, 4],"quiz_category":{"type":"science","id":"5"}}'`
- **sample response:**
``` json
{
  "question": {
    "answer": "Edward Scissorhands", 
    "category": 5, 
    "difficulty": 3, 
    "id": 6, 
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  }, 
  "success": true
}
```

### Error Handling
Errors are returned as JSON objects in the following format:
``` json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Unprocessable Entity
