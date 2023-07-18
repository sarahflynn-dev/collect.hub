from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash

db = "collection_schema"
class Collection:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.date_start = db_data['date_start']
        self.thumb = db_data['thumb']
        self.description = db_data['description']
        self.size = db_data['size']
        self.unit = db_data['unit']
        self.safety = db_data['safety']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None

    @classmethod
    def retrieve(cls):
        db = "collection_schema"
        query = """
                SELECT * FROM collections
                JOIN users on collections.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        collection_list = []
        for row in results:
            this_collection = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "dob": row['dob'],
                "email": row['email'],
                "username": row['username'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_collection.creator = User(user_data)
            collection_list.append(this_collection)
        return collection_list
    
    @classmethod
    def find_id(cls,data):
        query = """
                SELECT * FROM collections
                JOIN users on collections.user_id = users.id
                WHERE collections.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        current_collection = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        current_collection.creator = user.User(user_data)
        return current_collection
    @classmethod
    def store(cls, form_data):
        query = """
                INSERT INTO collections (title,date_start,thumb,description,size,unit,safety,user_id)
                VALUES (%(title)s,
                %(date_start)s,
                %(thumb)s,
                %(description)s,
                %(size)s,
                %(unit)s,
                %(safety)s,
                %(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)
    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE collections
                SET title = %(title)s,
                date_start = %(date_start)s,
                thumb = %(thumb)s,
                description = %(description)s,
                size = %(size)s,
                unit = %(unit)s,
                safety = %(safety)s,
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,form_data)
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM collections
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    @staticmethod
    def validate_collection(form_data):
        is_valid = True

        if len(form_data['title']) < 3:
            flash("Please provide a valid collection title.")
            is_valid = False
        if form_data['date_start'] == '':
            flash("Please provide a date.")
            is_valid = False
        if form_data['thumb'] == '':
            flash("Please upload a thumbnail.")
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(form_data['size']) < 1:
            flash("Please include a valid number.")
            is_valid = False
        if form_data['unit'] == '':
            flash("Please include a unit selection.")
            is_valid = False
        if form_data['safety'] == '':
            flash("Please provide an input.")
            is_valid = False
            
        return is_valid