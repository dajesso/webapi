from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow.fields import String, Date

class Animal(db.Model):
    tablename__ = 'animals'

    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))  # Link to Enclousre

    # Relationship with Enclousre model
    enclosures = db.relationship("Enclosure", back_populates="animals")


    # this is a test of foods

    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))  # Link to Enclousre

    # Relationship with Enclousre model
    foods = db.relationship("Food", back_populates="foods")
    

    #food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))  # Link to Enclousre

    # Relationship with food model
  #  food = db.relationship("Food", back_populates="foods")
#

    #name = db.Column(db.String(200), nullable=False)

    #fspecies = db.Column(db.String(200), nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    animal = db.Column(db.String(200), nullable=True)

    #animals = db.relationship("Animal", back_populates="foods")

    # Relationship with Enclousre model
    #enclosure = db.relationship("Enclosure", back_populates="animals")

    name = db.Column(db.String(200), nullable=False)
    species = db.Column(db.String(200), nullable=False)


class AnimalSchema(ma.Schema):
    name = String(required=True)
    
    zoo = fields.Nested('ZooSchema', many=True)
    enclosure = fields.Nested('EnclosureSchema', many=True)
    food = fields.Nested('FoodSchema', many=True)

    class Meta:
        fields =    ('id', 'name', 'food_id', 'enclosure_id', 'species')

one_animal = AnimalSchema()

many_animals = AnimalSchema(many=True)
animals_without_id = AnimalSchema(exclude=['id'])