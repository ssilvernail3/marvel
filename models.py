from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)





class User(db.Model):
    """Model to create a User"""

    __tablename__ = 'users'

    username = db.Column(db.String(25), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(40), nullable=True, unique=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    
    created = db.relationship('CreateHero')


    


    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False


class CreateHero(db.Model):
    """User created superhero / supervillain"""

    __tablename__ = 'created'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    name = db.Column(db.Text, nullable=False, unique=True)
    side = db.Column(db.Text, nullable=False)
    abilities = db.Column(db.Text, nullable=False)
    origin = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)
    
    username = db.Column(db.Text, db.ForeignKey('users.username'))
    
    user = db.relationship('User')
    