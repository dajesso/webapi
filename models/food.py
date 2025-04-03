from init import db, ma
from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow.fields import String, Date

class Food(db.Model):
    __tablename__ = "foods"
    
    #id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)

    #animals = db.relationship("Animal", back_populates="animals")

    foods = db.relationship("Animal", back_populates="foods")


    # Set back_populates to "enclousre" or the corresponding name in Animal model
    
    # Foreign key column to reference Enclousre table

    # Define the reverse relationship here
    #animals = db.relationship("Animal", back_populates="enclosure")

    price = db.Column(db.Integer, nullable=False)
    species = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    

class FoodSchema(ma.Schema):
    name = String(required=True)

    animal = fields.Nested('AnimalSchema', many=True)

    class Meta:
        fields = ('id', 'price', 'name', 'food_id')

one_food = FoodSchema()

many_foods = FoodSchema(many=True)
food_without_id = FoodSchema(exclude=['id'])