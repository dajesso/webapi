from flask import Blueprint
from init import db
from datetime import date

from models.animal import Animal
from models.enclosure import Enclosure
from models.food import Food
from models.zoo import Zoo


db_bp = Blueprint('db', __name__)

@db_bp.cli.command('init')
def create_tables():
    db.drop_all()
    db.create_all()
    print('Tables created')

@db_bp.cli.command('seed')
def seed_tables():
    foods = [
        Food(
            name='KFC Wings',
            price=69420,
            species="Panda",
        ),
        Food(
            name='Nuggets',
            price=32420,
            species="Human",
        )
    ]
    db.session.add_all(foods)
    db.session.commit()

    the_enclosures = [
        Enclosure(
            price=329420,
            species="panda",
            name="Panda View",
        ),
        Enclosure(
            price=329420,
            species="firefox",
            name="Feed foxes",
        )
    ]
    db.session.add_all(the_enclosures)
    db.session.commit()

    zoos = [
        Zoo(
            city="Adelaide",
            weather="25",
            name="Felicis zoo of Felicises",
            enclosures=[the_enclosures[0], the_enclosures[1]]  # Associate enclosures here
        ),

        Zoo(
            city="Melborune",
            weather="25",
            name="Obama zoo of Felicises",
            enclosures=[the_enclosures[1], the_enclosures[0]]  # Associate enclosures here
        ),

        Zoo(
            city="Sydney",
            weather="25",
            name="Felicis zoo of Felicises",
            enclosures=[the_enclosures[0], the_enclosures[1]]  # Associate enclosures here
        ),
    ]
    db.session.add_all(zoos)
    db.session.commit()  # Commit to save the relationships



    # No need to extend enclosures again
    # zoos[0].enclosures.extend(the_enclosures)  # Remove this line

    animals = [
        Animal(
            name='Felicis',
            enclosure_id=the_enclosures[0].id,
            food_id=foods[0].id,
            species='Panda',
            animal="Panda"
        ),
        Animal(
            name='Obama',
            enclosure_id=the_enclosures[1].id,
            food_id=foods[1].id,
            species='Obama',
            animal="Human",
        )
    ]
    db.session.add_all(animals)
    db.session.commit()

    print('Tables seeded')

    print(f"Zoo: {zoos[0].name}, Enclosures: {[enclosure.name for enclosure in zoos[0].enclosures]}")
    print(f"Zoo: {zoos[1].name}, Enclosures: {[enclosure.name for enclosure in zoos[0].enclosures]}")