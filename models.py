from flask import Flask, render_template, jsonify, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField
#from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text
import os
