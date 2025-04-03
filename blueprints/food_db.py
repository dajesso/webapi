from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.food import Food, many_foods, one_food, food_without_id

food_db = Blueprint('food_db', __name__)

#         fields = ('id', 'price', 'name', 'food_id')


@food_db.route('/foods')
def get_all_foods():
    stmt = db.select(Food).order_by(Food.name)
    food = db.session.scalars(stmt)
    return many_foods.dump(food)

@food_db.route('/foods/<int:food_id>')
def get_one_food(food_id):
    stmt = db.select(Food).filter_by(id=food_id)
    food = db.session.scalar(stmt)
    if food:
        return one_food.dump(food)
    else:
        return {'error': f'Food with id {food_id} does not exist'}, 404
    

@food_db.route('/foods', methods=['POST'])
def create_food():
    try:
        data = food_without_id.load(request.json)
        new_food = Food(
            name=data.get('name'),
            price=data.get('price')
        )
        db.session.add(new_food)
        db.session.commit()

        return one_food.dump(new_food)
    except Exception as err:
        return {"error": str(err)}, 400
    

@food_db.route('/foods/<int:food_id>', methods=['PUT', 'PATCH'])
def update_food(food_id):
    try:
        # Fetch the course by id
        stmt = db.select(Food).filter_by(id=food_id)
        new_food = db.session.scalar(stmt)
        if new_food:
            # Get incoming request body (JSON)
            data = food_without_id.load(request.json)
            # Update the attributes of the course with the incoming data
            new_food.name = data.get('name') or new_food.name
            new_food.price = data.get('price') or new_food.price
            # Commit the session
            db.session.commit()
            # Return the new Course instance
            return one_food.dump(new_food)
        else:
            return {'error': f'Food with id {food_id} does not exist'}, 404 
    except Exception as err:
        return {"error": str(err)}, 400


# Delete - DELETE /courses/<int:id>
@food_db.route('/foods/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    stmt = db.select(Food).filter_by(id=food_id)
    new_food = db.session.scalar(stmt)
    if new_food:
        db.session.delete(new_food)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Food with id {new_food} does not exist'}, 404 
   