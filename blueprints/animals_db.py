from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.animal import Animal, many_animals, one_animal, animals_without_id

animals_db = Blueprint('animals_db', __name__)

@animals_db.route('/animals')
def get_all_animals():
    stmt = db.select(Animal).order_by(Animal.name)
    animals = db.session.scalars(stmt)
    return many_animals.dump(animals)

@animals_db.route('/animals', methods=['POST'])
def create_animals():
    try:
        data = animals_without_id.load(request.json)
        new_animal = Animal(
            name=data.get('name'),
            species=data.get('species'),
            enclosure_id=data.get('enclosure_id'),
            food_id=data.get('food_id')
        )
        db.session.add(new_animal)
        db.session.commit()

        return one_animal.dump(new_animal)
    except Exception as err:
        return {"error": str(err)}, 400

@animals_db.route('/animals/<int:animal_id>')
def get_one_animal(animal_id):
    stmt = db.select(Animal).filter_by(id=animal_id)
    animal = db.session.scalar(stmt)
    if animal:
        return one_animal.dump(animal)
    else:
        return {'error': f'Animal with id {animal_id} does not exist'}, 404
        

@animals_db.route('/animals/<int:animal_id>', methods=['PUT', 'PATCH'])
def update_animal(animal_id):
    try:
        # Fetch the course by id
        stmt = db.select(Animal).filter_by(id=animal_id)
        new_animal = db.session.scalar(stmt)
        if new_animal:
            # Get incoming request body (JSON)
            data = animals_without_id.load(request.json)
            # Update the attributes of the course with the incoming data
            new_animal.name = data.get('name') or new_animal.name
            new_animal.species = data.get('species') or new_animal.speices
            new_animal.enclosure_id = data.get('enclosure_id') or new_animal.enclosure_id
            new_animal.food_id = data.get('food_id', new_animal.food_id)
            # Commit the session
            db.session.commit()
            # Return the new Course instance
            return one_animal.dump(new_animal)
        else:
            return {'error': f'Animal with id {animal_id} does not exist'}, 404 
    except Exception as err:
        return {"error": str(err)}, 400


# Delete - DELETE /courses/<int:id>
@animals_db.route('/animals/<int:animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    stmt = db.select(Animal).filter_by(id=animal_id)
    new_animal = db.session.scalar(stmt)
    if new_animal:
        db.session.delete(new_animal)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Animal with id {animal_id} does not exist'}, 404 
   