# databootcamp-miniproject1

Python OOP Mini-Project: Banking System Case Study

## Setup

- create database:

```
CREATE DATABASE bankdemo;

```

- create an .env file with a db connection string:

```
DB_CONNECTION_STRING=mysql://{your_username}:{your_password}@localhost/bankdemo
```

## Run

```
python3 main.py
```

Note: you will need to run this once to create the tables, and then add an employee manually into the database.

```
INSERT INTO employee (first_name, last_name, email, is_manager, department) VALUES ('<firstname>', '<lastname>', '<email>', <true / false>, '<dept name>');
```

Once this is done, you can add additional employees and customers within the app.
