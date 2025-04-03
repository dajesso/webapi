from flask import Flask
from init import db, ma
from marshmallow.exceptions import ValidationError
from dotenv import load_dotenv
import os
from blueprints.db_bp import db_bp
from blueprints.animals_db import animals_db
from blueprints.food_db import food_db
from blueprints.enclosure_db import enclosure_db
from blueprints.zoo_db import zoo_db



def create_app():
    app = Flask(__name__)

    load_dotenv(override=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')


    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_bp)
    app.register_blueprint(animals_db)
       
    app.register_blueprint(food_db)

    app.register_blueprint(enclosure_db)

    app.register_blueprint(zoo_db)


    return app