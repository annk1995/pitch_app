from flask import Blueprint

# instantiate the Blueprint
main = Blueprint( 'main',__name__)

from . import views