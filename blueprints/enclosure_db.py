from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.enclosure import EnclosureSchema, many_enclosures, one_enclosure, enclosure_without_id
from models.enclosure import Enclosure

enclosure_db = Blueprint('enclosure_db', __name__)

@enclosure_db.route('/enclosures')
def get_all_enclosures():
    stmt = db.select(Enclosure).order_by(Enclosure.name)
    one_enclosures = db.session.scalars(stmt)
    return many_enclosures.dump(one_enclosures)


#        fields = ('id', 'price', 'species', 'name', 'animal_id', 'zoo_id')


@enclosure_db.route('/enclosures', methods=['POST'])
def create_enclosure():
    try:
        data = enclosure_without_id.load(request.json)
        new_enclosure = Enclosure(
            name=data.get('name'),
            species=data.get('species'),
            price = data.get('price'),
            zoo_id = data.get('zoo_id')
        )
        db.session.add(new_enclosure)
        db.session.commit()

        return one_enclosure.dump(new_enclosure)
    except Exception as err:
        return {"error": str(err)}, 400

@enclosure_db.route('/enclosures/<int:enclosure_id>')
def get_one_enclosure(enclosure_id):
    stmt = db.select(Enclosure).filter_by(id=enclosure_id)
    enclosures = db.session.scalar(stmt)
    if enclosures:
        return one_enclosure.dump(enclosures)
    else:
        return {'error': f'Enclosure with id {enclosure_id} does not exist'}, 404
        

@enclosure_db.route('/enclosures/<int:enclosure_id>', methods=['PUT', 'PATCH'])
def update_enclosure(enclosure_id):
    try:
        # Fetch the enclosure by id
        stmt = db.select(Enclosure).filter_by(id=enclosure_id)
        new_enclosure = db.session.scalar(stmt)
        if new_enclosure:
            # Get incoming request body (JSON)
            data = enclosure_without_id.load(request.json)
            # Update the attributes of the course with the incoming data
            new_enclosure.name = data.get('name') or new_enclosure.name
            new_enclosure.species = data.get('species') or new_enclosure.speices
            new_enclosure.zoo_id = data.get('zoo_id') or new_enclosure.zoo_id
            # Commit the session
            db.session.commit()
            # Return the new Course instance
            return one_enclosure.dump(new_enclosure)
        else:
            return {'error': f'Enclosure with id {enclosure_id} does not exist'}, 404 
    except Exception as err:
        return {"error": str(err)}, 400


# Delete - DELETE /courses/<int:id>
@enclosure_db.route('/enclosures/<int:enclosure_id>', methods=['DELETE'])
def delete_enclosure(enclosure_id):
    stmt = db.select(Enclosure).filter_by(id=enclosure_id)
    new_enclosure = db.session.scalar(stmt)
    if new_enclosure:
        db.session.delete(new_enclosure)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Enclosure  with id {enclosure_id} does not exist'}, 404 
   