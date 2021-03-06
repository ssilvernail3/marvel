from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, CreateHero
from forms import RegisterUserForm, UserForm, SuperHeroForm
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

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """ Displays template for MarvelPedia homepage """

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
            return redirect('/')

        else:
            form.username.errors = ['Invalid username / password']
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    '''Logout User'''
    session.pop('username')
    flash('Goodbye! See you again soon!', 'warning')
    return redirect('/login')

@app.route('/users/<username>', methods=['GET', 'POST'])
def user_info(username):
    '''GET request render form for creating new super / POST request handles form submission'''
    user = User.query.get_or_404(username)

    if 'username' not in session:
        flash('Please Login First!', 'danger')
        return redirect('/login')

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
    '''GET request renders edit form for super / POST request handles form submission'''

    supers = CreateHero.query.get_or_404(super_id)
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
    '''Deletes created super'''
    
    supers = CreateHero.query.get(super_id)

    if 'username' not in session:
        flash('Please Login First!', 'danger')
        return redirect('/login')

    db.session.delete(supers)
    db.session.commit()

    return redirect(f'/users/{supers.username}')