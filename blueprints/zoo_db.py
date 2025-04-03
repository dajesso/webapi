from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.zoo import ZooSchema, many_zoos, one_zoo, zoo_without_id
from models.zoo import Zoo
from models.enclosure import Enclosure
import asyncio


zoo_db = Blueprint('zoo_db', __name__)


@zoo_db.route('/zoos')
def get_all_zoos():
    stmt = db.select(Zoo).order_by(Zoo.name)
    zoos = db.session.scalars(stmt).all()
    return many_zoos.dump(zoos)

@zoo_db.route('/zoos/<int:zoo_id>')
def get_one_zoo(zoo_id):
    stmt = db.select(Zoo).filter_by(id=zoo_id)
    zoos = db.session.scalar(stmt)
    if zoos:
        return one_zoo.dump(zoos)
    else:
        return {'error': f'Zoo with id {zoo_id} does not exist'}, 404
    

@zoo_db.route('/zoos', methods=['POST'])
def create_zoo():
    try:
        # Load data from the request
        data = zoo_without_id.load(request.json)

        # Create a new Zoo object
        new_zoo = Zoo(
            name=data.get('name'),
            city=data.get('city'),
            weather=data.get('weather')
        )

        # Handle enclosures if provided
        enclosures_data = data.get('enclosures', [])
        for enclosure_data in enclosures_data:
            # Check if the enclosure already exists (by ID or unique fields)
            enclosure = Enclosure.query.filter_by(
                name=enclosure_data.get('name'),
                species=enclosure_data.get('species')
            ).first()

            # If the enclosure doesn't exist, create a new one
            if not enclosure:
                enclosure = Enclosure(
                    name=enclosure_data.get('name'),
                    species=enclosure_data.get('species'),
                    price=enclosure_data.get('price')
                )
                db.session.add(enclosure)

            # Associate the enclosure with the zoo
            new_zoo.enclosures.append(enclosure)

        # Add the new Zoo to the session and commit
        db.session.add(new_zoo)
        db.session.commit()

        # Return the serialized Zoo object
        return one_zoo.dump(new_zoo), 201
    except Exception as err:
        return {"error": str(err)}, 400
    
@zoo_db.route('/zoos/<int:zoo_id>', methods=['PUT', 'PATCH'])
def update_zoo(zoo_id):
    try:
        # Fetch the Zoo by ID
        stmt = db.select(Zoo).filter_by(id=zoo_id)
        zoo = db.session.scalar(stmt)

        if zoo:
            # Get incoming request body (JSON)
            data = zoo_without_id.load(request.json)

            # Update the Zoo attributes
            zoo.name = data.get('name') or zoo.name
            zoo.city = data.get('city') or zoo.city
            zoo.weather = data.get('weather') or zoo.weather

            # Handle enclosures if provided
            enclosures_data = data.get('enclosures', [])
            updated_enclosures = []

            for enclosure_data in enclosures_data:
                # Check if the enclosure already exists (by ID or unique fields)
                enclosure = Enclosure.query.filter_by(
                    name=enclosure_data.get('name'),
                    species=enclosure_data.get('species')
                ).first()

                # If the enclosure doesn't exist, create a new one
                if not enclosure:
                    enclosure = Enclosure(
                        name=enclosure_data.get('name'),
                        species=enclosure_data.get('species'),
                        price=enclosure_data.get('price')
                    )
                    db.session.add(enclosure)

                # Add the enclosure to the updated list
                updated_enclosures.append(enclosure)

            # Update the Zoo's enclosures
            zoo.enclosures = updated_enclosures

            # Commit the session
            db.session.commit()

            # Return the updated Zoo instance
            return one_zoo.dump(zoo), 200
        else:
            return {'error': f'Zoo with id {zoo_id} does not exist'}, 404
    except Exception as err:
        return {"error": str(err)}, 400

# Delete - DELETE /courses/<int:id>
@zoo_db.route('/zoos/<int:zoo_id>', methods=['DELETE'])
def delete_food(zoo_id):
    stmt = db.select(Zoo).filter_by(id=zoo_id)
    new_zoo = db.session.scalar(stmt)
    if new_zoo:
        db.session.delete(new_zoo)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Zoo with id {new_zoo} does not exist'}, 404 
   