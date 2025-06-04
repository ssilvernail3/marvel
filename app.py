from flask import Flask, render_template, redirect, session, flash, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, CreateHero
from forms import RegisterUserForm, UserForm, SuperHeroForm
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import requests
import hashlib
import time


load_dotenv()

API_BASE_URL = "https://gateway.marvel.com/"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

bcrypt = Bcrypt()
connect_db(app)
#toolbar = DebugToolbarExtension(app)

# -------------------------------
# PUBLIC ROUTES
# -------------------------------

@app.route('/')
def home_page():
    """Displays MarvelPedia homepage - PUBLIC"""
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user - PUBLIC"""
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data   
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_User = User.register(username, password, email, first_name, last_name)
        db.session.add(new_User)

        try: 
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username is already taken, please try again!')
            return render_template('register.html', form=form)

        session['username'] = username
        flash('Congratulations! You have created a new account!', 'success')
        return redirect('/')  # redirect to homepage

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login - PUBLIC"""
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f'Welcome back {user.username}!', 'success')
            session['username'] = username
            return redirect('/')
        else:
            form.username.errors = ['Invalid username / password']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('username')
    flash('Goodbye! See you again soon!', 'warning')
    return redirect('/login')

# -------------------------------
# PROTECTED ROUTES
# -------------------------------

@app.route('/users/<username>', methods=['GET', 'POST'])
def user_info(username):
    """Protected: User's Superhero creation page"""
    if 'username' not in session or session['username'] != username:
        flash('Please log in to access this page.', 'danger')
        return redirect('/login')

    user = User.query.get_or_404(username)
    form = SuperHeroForm()

    if form.validate_on_submit():
        name = form.name.data
        side = form.side.data
        abilities = form.abilities.data
        origin = form.origin.data
        image_url = form.image_url.data

        new_Super = CreateHero(name=name, side=side, abilities=abilities, origin=origin, image_url=image_url, username=username)
        db.session.add(new_Super)
        db.session.commit()
        return redirect(f'/users/{user.username}')
        
    return render_template('users/user.html', user=user, form=form)

@app.route('/<int:super_id>/edit', methods=['GET', 'POST'])
def modify_super(super_id):
    """Protected: Edit Superhero"""
    supers = CreateHero.query.get_or_404(super_id)

    if 'username' not in session or session['username'] != supers.username:
        flash('Please log in to access this page.', 'danger')
        return redirect('/login')

    form = SuperHeroForm(obj=supers)

    if form.validate_on_submit():
        supers.name = form.name.data
        supers.side = form.side.data
        supers.abilities = form.abilities.data
        supers.origin = form.origin.data
        supers.image_url = form.image_url.data

        flash(f'{supers.name} has been updated!')
        db.session.commit()
        return redirect(f'/users/{supers.username}')

    return render_template('users/edit_super.html', form=form)

@app.route('/<int:super_id>/delete', methods=['POST'])
def delete_super(super_id):
    """Protected: Delete Superhero"""
    supers = CreateHero.query.get_or_404(super_id)

    if 'username' not in session or session['username'] != supers.username:
        flash('Please log in to access this page.', 'danger')
        return redirect('/login')

    db.session.delete(supers)
    db.session.commit()
    flash(f'{supers.name} has been deleted!', 'warning')
    return redirect(f'/users/{supers.username}')

# -------------------------------
# API SEARCH ROUTE
# -------------------------------

@app.route('/api/search')
def api_search():
    """Server-side Marvel API proxy to avoid CORS, with retry logic"""

    character_name = request.args.get('name', '')

    ts = str(int(time.time()))
    public_key = os.environ.get('MARVEL_PUBLIC_KEY')
    private_key = os.environ.get('MARVEL_PRIVATE_KEY')

    # Debug prints to confirm keys:
    print(f"DEBUG - MARVEL_PUBLIC_KEY: {public_key}")
    print(f"DEBUG - MARVEL_PRIVATE_KEY: {private_key}")

    if not public_key or not private_key:
        return jsonify({'error': 'Missing Marvel API keys'}), 500

    to_hash = ts + private_key + public_key
    hash_digest = hashlib.md5(to_hash.encode('utf-8')).hexdigest()

    marvel_url = 'https://gateway.marvel.com/v1/public/characters'

    params = {
        'name': character_name,
        'ts': ts,
        'apikey': public_key,
        'hash': hash_digest
    }

    max_retries = 3
    retry_delay = 2  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt}: Fetching from Marvel API...")
            resp = requests.get(marvel_url, params=params)
            resp.raise_for_status()  # raise error for 4xx/5xx
            print(f"Success on attempt {attempt}")
            data = resp.json()
            return jsonify(data)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP Error: {http_err} (Status code: {resp.status_code})")
            if resp.status_code == 504 and attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                continue
            else:
                return jsonify({'error': 'Marvel API error', 'details': str(http_err)}), resp.status_code

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return jsonify({'error': 'Marvel API request failed', 'details': str(e)}), 500

    # If loop exhausted retries:
    return jsonify({'error': 'Marvel API request failed after retries'}), 504