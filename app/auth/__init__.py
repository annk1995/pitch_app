from flask import Blueprint

auth = Blueprint('auth', __name__)  # create a Blueprint instance auth
from . import views