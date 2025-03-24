from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import sqlalchemy

app = Flask(__name__)  # Remova instance_relative_config=True

# Diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# URI do Banco de Dados (Aponta para a raiz do projeto)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'community.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '57024a46c4f67b94e911c0319fabe56e'
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'community.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from secretcommunity import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)

if not inspector.has_table('user'):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print('Database created')
else:
    print('Database already exists')

from secretcommunity import routes
from secretcommunity import models