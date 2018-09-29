# coding=utf-8

from flask import Blueprint

express = Blueprint('express', __name__)

import app.express.views
