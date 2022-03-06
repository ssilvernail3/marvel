from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)





class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(25), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(40), nullable=True, unique=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    
    # dob = db.Column(db.Integer, nullable=False)


    favorites = db.relationship('UserFavorites')


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


class UserFavorites(db.Model):
    """User Favorites table"""

    __tablename__ = 'favorites'

    user = db.Column(db.Text, db.ForeignKey('users.username'))
    name = db.Column(db.Text, nullable=False, primary_key=True)
    description = db.Column(db.Text)

    users = db.relationship('User')



