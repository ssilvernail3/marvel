from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterUserForm, UserForm
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

API_BASE_URL = "https://gateway.marvel.com/"




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///marvel"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

bcrypt = Bcrypt()

# CURR_USER_KEY = "curr_user"


connect_db(app)

toolbar = DebugToolbarExtension(app)


# @app.before_request
# def add_user_to_g():
#     """If we're logged in, add curr user to Flask global."""

#     if CURR_USER_KEY in session:
#         user = User.query.get(session[CURR_USER_KEY])

#     else:
#         user = None


# def do_login(user):
#     """Log in user."""

#     session[CURR_USER_KEY] = user.id


# def do_logout():
#     """Logout user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]




@app.route('/')
def home_page():
    """ Displays template for app homepage """

    if 'username' not in session:
        flash('Please Login First!', 'danger')
        return redirect('/login')

    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''GET request to render register form / POST request to register User'''
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

        return redirect(f'/users/{username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''GET request to render login form / POST request handle login form submission'''

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
    
        if user:
            flash(f'Welcome Back {user.username}', 'success')
            session['username'] = username
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ['Invalid username / password']
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    '''Logout User'''
    session.pop('username')
    flash('Goodbye! See you again soon!', 'warning')
    return redirect('/login')

@app.route('/users/<username>')
def user_info(username):
    '''GET request shows User info / feedback'''
    user = User.query.get_or_404(username)

    if 'username' not in session:
        flash('Please Login First!', 'danger')
        return redirect('/login')

    return render_template('users/user.html', user=user)


# @app.route('/search')
# def search():
#     term = request.args['search']
#     return redirect(f'https://gateway.marvel.com/v1/public/characters?name={term}&ts=1&apikey=9fc66a02b7eaad221022d19aee14503d&hash=14bc49d69eac6d1dd823e2e75394321a')


@app.route('/users/<username>/add_favorite', methods=["POST"])
def add_favorite(username):

    user = User.query.get_or_404(username)

    if 'username' not in session:
        flash('Please Login First!', 'danger')
        return redirect('/login')


    
    return redirect(f'/users/{user.username}/favorties')

@app.route('/favorite')
def show_favorite():

    return render_template('favorite.html')