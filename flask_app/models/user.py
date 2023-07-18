from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
USERNAME_REGEX = re.compile(r'\A[\w\-\.]{3,}\Z')

db = "collection_schema"
#define User class
class User:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.dob = db_data['dob']
        self.email = db_data['email']
        self.username = db_data['username']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

#classmethod to submit data
    @classmethod
    def store(cls,form_data):
        hashed_data = {
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'dob': form_data['dob'],
            'email': form_data['email'],
            'username': form_data['username'],
            'password': bcrypt.generate_password_hash(form_data['password']),
        }
        query = """
                INSERT INTO users (first_name,last_name,dob,username,email,password)
                VALUES (%(first_name)s,
                %(last_name)s,
                %(dob)s,
                %(username)s,
                %(email)s,
                %(password)s);
                """
        return connectToMySQL(db).query_db(query,hashed_data)

#classmethod to find user by email
    @classmethod
    def find_email(cls,data):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False
        return cls(result[0])
    
#classmethod to find user by username
    @classmethod
    def find_username(cls,data):
        query = """
                SELECT * FROM users
                WHERE username = %(username)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False
        return cls(result[0])

#classmethod to lookup by id
    @classmethod
    def find_id(cls,data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        return cls(result[0])

#validate our logins for errors
    @staticmethod
    def validate_registration(form_data):
        is_valid = True

        if len(form_data['email']) < 1:
            flash("Please enter a valid email address.","register")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email address.","register")
            is_valid = False
        elif not USERNAME_REGEX.match(form_data['username']):
            flash("Invalid username.","register")
            return False
        elif User.find_email(form_data):
            flash("This email is taken. Please try another.","register")
            is_valid = False
        elif User.find_username(form_data):
            flash("This username is taken. Please try another.","register")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters.","register")
            is_valid = False
        if form_data['password'] != form_data['confirm']:
            flash("Passwords do not match.","register")
            is_valid = False
        if len(form_data['first_name']) < 2:
            flash("First name must be at least 2 characters.","register")
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("Last name must be at least 2 characters.","register")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(form_data):

        # if not EMAIL_REGEX.match(form_data['email']):
        #     flash("Invalid email or password.","login")
        #     return False
        
        if not USERNAME_REGEX.match(form_data['username']):
            flash("Invalid username or password.","login")
            return False

        user = User.find_username(form_data)
        if not user:
            flash("Invalid username or password.","login")
            return False
        
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash("Invalid username or password.","login")
            return False
        
        return user