from secretcommunity import database, login_manager
from datetime import datetime
import pytz
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    user = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), nullable=False, unique=True)
    password = database.Column(database.String(255), nullable=False)
    photo_profile = database.Column(database.String(100), default='default.jpg')
    posts = database.relationship('Post', backref='author', lazy=True)
    subjects = database.Column(database.String, nullable=False, default='None')

    def count_posts(self):
        return len(self.posts)


class Post(database.Model):
    post_id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(50), nullable=False)
    body = database.Column(database.Text, nullable=False)
    date_created = database.Column(database.DateTime, nullable=False, default=datetime.now(pytz.timezone('America/Sao_Paulo')))
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)



