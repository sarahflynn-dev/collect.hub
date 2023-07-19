from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session
from flask_app.models.collection import Collection
from flask_app.models.user import User

from werkzeug.utils import secure_filename
import os

db = "collection_schema"

#boot user from dashboard if not logged in
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.find_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')   
    return render_template('dashboard.html', user=user, collections=Collection.retrieve())

@app.route('/browse')
def render_browse():
    # if 'user_id' in session:
    #     return render_template('browse.html')
    #     return redirect('/login')
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('browse.html', user=User.find_id({"id":session['user_id']}), collections=Collection.retrieve())

#boot user from making a new entry if not logged in
@app.route('/new/collection')
def create_collection():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('new_collect.html', user=User.find_id({"id":session['user_id']}))

@app.route('/new/collection/process', methods=['POST'])
def process_collection():
    if 'user_id' not in session:
        return redirect('/login')
    if not Collection.validate_collection(request.form,request.files):
        return redirect('/new/collection')
    # print({"id":session['user_id']})
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!", request.files['thumbnail'])
    data = {
        # 'id': id,
        'title': request.form['title'],
        'date_start': request.form['date_start'],
        'thumbnail': request.files['thumbnail'],
        'description': request.form['description'],
        'size': request.form['size'],
        'unit': request.form['unit'],
        'safety': request.form['safety'],
        'user_id':session["user_id"],
    }
    Collection.store(data)
    return redirect('/dashboard')

@app.route('/view/<int:id>')
def view_collection(id):
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('view_collect.html',user=User.find_id({"id":session['user_id']}),collection=Collection.find_id({'id': id}))

@app.route('/edit/<int:id>')
def edit_collection(id):
    if 'user_id' not in session:
        return redirect('/login')

    return render_template('edit_collect.html',collection=Collection.find_id({'id': id}), user=User.find_id({"id":session['user_id']}))

@app.route('/edit/process/<int:id>', methods=['POST'])
def process_edit_collection(id):
    if 'user_id' not in session:
        return redirect('/login')
    if not Collection.validate_collection(request.form, request.files):
        return redirect(f'/edit/{id}')
    data = {
        'id': id,
        'title': request.form['title'],
        'date_start': request.form['date_start'],
        'thumbnail': request.files['thumbnail'],
        'description': request.form['description'],
        'size': request.form['size'],
        'unit': request.form['unit'],
        'safety': request.form['safety'],
    }
    Collection.update(data)
    return redirect('/dashboard')

@app.route('/destroy/<int:id>')
def destroy_collection(id):
    if 'user_id' not in session:
        return redirect('/login')
    Collection.destroy({'id':id})
    return redirect('/dashboard')