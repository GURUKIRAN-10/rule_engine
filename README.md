# Rule Engine Application

## Overview

The Rule Engine application is a dynamic web-based system that evaluates user-defined rules using an Abstract Syntax Tree (AST) structure. This project supports rule creation, modification, and evaluation through a user-friendly web interface and RESTful APIs. It allows the user to define rules and evaluate them against user data.

## Features

- **Create Dynamic Rules**: Users can define rules using a simple expression syntax.
- **Rule Evaluation**: Rules can be evaluated against user data.
- **AST Representation**: The rules are represented and processed using an Abstract Syntax Tree (AST).
- **API Support**: RESTful APIs allow interaction with the rule engine programmatically.
- **Web-based Interface**: Users can create and evaluate rules directly in the browser.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running the Application](#running-the-application)
4. [Project Structure](#project-structure)
5. [API Endpoints](#api-endpoints)
6. [Testing the Application](#testing-the-application)
7. [Design Choices](#design-choices)
8. [Non-functional Considerations](#non-functional-considerations)
9. [Future Enhancements](#future-enhancements)

---

## Prerequisites

Before running the application, ensure that you have the following installed:

- **Python 3.7+**
- **Git**
- **Virtual Environment** (Optional but recommended)

You may also use tools like **Postman** or **cURL** to test the API endpoints.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/GURUKIRAN-10/rule_engine.git
cd rule_engine

2. Set Up a Virtual Environment (Optional but Recommended)


Windows:
bash
python -m venv venv
venv\Scripts\activate

Mac/Linux:
bash

python3 -m venv venv
source venv/bin/activate


This will install Flask, SQLAlchemy, and other necessary dependencies.

4. Set Up the Database
The project uses an SQLite database. To set it up, run the following command to initialize the database schema

python -c "from src.database import Base, engine; Base.metadata.create_all(engine)"

This will create a new SQLite database file rules.db in the src/ directory.

Running the Application

1. Start the Flask Development Server
Run the following command to start the web server:

bash

flask run --debug
By default, the application will be available at http://127.0.0.1:5000/.

You can open your browser and navigate to this URL to interact with the web interface for creating and evaluating rules.

Project Structure
graphql

rule_engine/
│
├── venv/                        # Virtual environment files (optional)
├── src/
│   ├── api.py                   # Main Flask API for handling requests
│   ├── database.py              # Database models and setup
│   ├── evaluator.py             # Core evaluation logic for rules
│   ├── node.py                  # AST node structure
│   ├── optimizer.py             # (Optional) Optimizer for AST manipulation
│   ├── static/
│   │   ├── script.js            # Frontend JavaScript code
│   │   └── styles.css           # Frontend styling
│   └── templates/
│       └── index.html           # HTML for the web interface
│   └── rules.db                 # SQLite database file
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation (this file)


API Endpoints
1. Create Rule: POST /create_rule
Creates a new rule for evaluation.

Request Body:
{
    "rule_ast": {
        "node_type": "operator",
        "value": "AND",
        "left": {
            "node_type": "operand",
            "value": "age > 18"
        },
        "right": {
            "node_type": "operand",
            "value": "income > 50000"
        }
    }
}

Response:

{
    "message": "Rule created successfully."
}


2. Evaluate Rule: POST /evaluate
Evaluates user data against the defined rule.

Request Body:
{
    "user_data": {
        "age": 25,
        "income": 60000
    },
    "rule_ast": {
        "node_type": "operator",
        "value": "AND",
        "left": {
            "node_type": "operand",
            "value": "age > 18"
            },
        "right": {
            "node_type": "operand",
            "value": "income > 50000"
        }
    }
}

Response:

json

{
    "result": true
}

Testing the Application
You can test the rule creation and evaluation via the web interface or using a tool like Postman or cURL.

Example: Using Postman
Create Rule: Send a POST request to http://127.0.0.1:5000/create_rule with the rule AST in the request body.
Evaluate Rule: Send a POST request to http://127.0.0.1:5000/evaluate with user data and rule AST.
```

Design Choices
Abstract Syntax Tree (AST): The use of AST for representing rules allows flexibility in dynamically creating, combining, and evaluating complex rules.
Modular Codebase: Each module handles a specific responsibility, such as evaluation logic (evaluator.py), API handling (api.py), and database management (database.py).
REST API: The rule engine is built as a RESTful service, making it easy to integrate with other systems.

Test Case 1
Rule:

plaintext

"((age > 30 AND department = 'Sales')) AND (salary > 50000 OR experience > 5)"
User Data:

json

{
"age": 32,
"department": "Sales",
"salary": 60000,
"experience": 4
}
Expected Result:

json

true
Corresponding AST
AST:

json

{
"node_type": "operator",
"value": "AND",
"left": {
"node_type": "operator",
"value": "AND",
"left": {
"node_type": "operand",
"value": "age > 30"
},
"right": {
"node_type": "operand",
"value": "department = 'Sales'"
}
},
"right": {
"node_type": "operator",
"value": "OR",
"left": {
"node_type": "operand",
"value": "salary > 50000"
},
"right": {
"node_type": "operand",
"value": "experience > 5"
}
}
}
Explanation
Evaluation Steps:

Left Side of AND:
Evaluate age > 30:
32 > 30 → True
Evaluate department = 'Sales':
"Sales" = "Sales" → True
Result of Left Side:
True AND True → True

Right Side of AND:
Evaluate salary > 50000:
60000 > 50000 → True
Evaluate experience > 5:
4 > 5 → False
Result of Right Side:
True OR False → True
Final Result:

True AND True → True

Test Case 2
Rule:

plaintext

"((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
User Data:

json

{
"age": 32,
"department": "Sales",
"salary": 60000,
"experience": 4
}
Expected Result:

json

false
Corresponding AST
AST:

json

{
"node_type": "operator",
"value": "AND",
"left": {
"node_type": "operator",
"value": "AND",
"left": {
"node_type": "operand",
"value": "age > 30"
},
"right": {
"node_type": "operand",
"value": "department = 'Marketing'"
}
},
"right": {
"node_type": "operator",
"value": "OR",
"left": {
"node_type": "operand",
"value": "salary > 20000"
},
"right": {
"node_type": "operand",
"value": "experience > 5"
}
}
}
Explanation
Evaluation Steps:

Left Side of AND:
Evaluate age > 30:
32 > 30 → True
Evaluate department = 'Marketing':
"Sales" = "Marketing" → False
Result of Left Side:
True AND False → False

Right Side of AND:
Evaluate salary > 20000:
60000 > 20000 → True
Evaluate experience > 5:
4 > 5 → False
Result of Right Side:
True OR False → True
Final Result:

False AND True → False
