# shipay-user-api

An awesome Mood Sensing APP

# API Documentation
We use swagger to documentation our API. The swagger provides all information we need to use our routes

## How its work
This project is a Clean-Architecture based. We have 3 important layers
1. Frameworks: responsible for all interactions with the external world
2. Interface Adapters: responsible for adapt the external world into business logic
3. Domain (Applicaion + entities): responsible for create and exec all business logic in fact

In this project we have: FastAPI, Dependency-Injector, SqlAlchemy, Poetry, Docker, Postgres, Pydantic, Alembic

# How to start?

IMPORTANT.: See the `makefile` (please, use make style to get a better code)to get to know some alias and follow the commands

1. We use poetry to deal with dependency management, so take a look in poetry documentation for more details. To create an environment, run:
    1. poetry shell - create/activate a new environment
    2. poetry install - install project dependencies

2. Using Makefile, please run as following
    1. make db_up (this will create our awesome postgres database)
    2. make db_create_tables (wait untill database is online - this will create our tables using alembic)

3. Now we have our database setting up and stored, lets run our application
    1. make run (without debug)
    2. make debug (to see the FastAPI debug)

4. Take a look at swagger accesing /docs on your local to see our routes
    example: https:localhost:8000/docs
