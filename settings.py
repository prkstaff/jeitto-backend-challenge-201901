from flask import Flask
import logging
import sys
import os
from flasgger import Swagger

# Environment

# Logging
logger = logging.getLogger('flask')
sh = logging.StreamHandler(sys.stdout)
logger_level = logging.DEBUG if os.getenv("FLASK_ENV") == "development" else logging.INFO
logger.setLevel(logger_level)
logger.addHandler(sh)

# App
app = Flask(__name__)
swagger = Swagger(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "4j%5qm*d1@lwhk_8dqib39hg!)!=inkr&8=90p4-&l*363+q_s")
