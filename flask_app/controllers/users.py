from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User

@app.route('/')
def redirect_index():
    return redirect('/index')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/bookmarks')
def manage():
    return render_template('bookmarks.html')

@app.route('/new/collection')
def new_collection():
    return render_template('new_collect.html')

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('register.html')

@app.route('/login/redirect', methods=['POST'])
def login_success():
    user = User.validate_login(request.form)
    if not user:
        return redirect('/dashboard')

    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/register/redirect', methods=['POST'])
def register_success():
    if not User.validate_registration(request.form):
        return redirect('/dashboard')

    user_id = User.store(request.form)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/login')