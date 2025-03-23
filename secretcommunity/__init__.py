from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate  # Importe o Flask-Migrate

app = Flask(__name__)

# Diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# URI do Banco de Dados (Prioriza a variável de ambiente DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'community.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '57024a46c4f67b94e911c0319fabe56e'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

migrate = Migrate(app, database)  # Inicialize o Flask-Migrate

from secretcommunity import routes
from secretcommunity import models

# Cria as tabelas do banco de dados dentro do contexto da aplicação
with app.app_context():
    database.create_all()