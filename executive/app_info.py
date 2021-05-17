from flask import Flask as f
from flask_sqlalchemy import SQLAlchemy

app = f(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///actions/executive.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret key"

db = SQLAlchemy(app)