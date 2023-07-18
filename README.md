# PyQt6 Recipe Book

A recipe book made using PyQt6 that uses postgresql database. It has options 
to add, remove, and view recipes with ease.

## Instructions
- Clone the repo
- Create a config.ini in the config directory
- Use config/recipe.sql to create a database table
- Run: python main.py

## Example config.ini
~~~
[postgresql]
host = your_host
user = your_username
db = your_db_name
pass = your_password
port = 5432
~~~

## Coming Features
- An edit option while viewing recipes
- Advanced styling options
- Pictures for recipes
