from init import db, ma
from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow.fields import String, Date
from models.association import zoo_enclosure

class Enclosure(db.Model):
    __tablename__ = "enclosures"
    enclosure_id = db.ForeignKey('enclosures.id')

    #id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)

    
    animals = db.relationship("Animal", back_populates="enclosures")

    # Set back_populates to "enclousre" or the corresponding name in Animal model
    
    # Foreign key column to reference Enclousre table

    # Define the reverse relationship here
    #animals = db.relationship("Animal", back_populates="enclosure")

    #zoos = db.relationship("Zoo", back_populates="enclosures")

    

    price = db.Column(db.Integer, nullable=False)
    species = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)

    #zoo_id = db.Column(db.Integer, db.ForeignKey('zoos.id'))

    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))

    zoo_id = db.Column(db.Integer, db.ForeignKey('zoos.id'))

    # test

    #zoos = db.relationship(
   #     'Zoo',
    #    secondary='association_table',
    #    primaryjoin='Enclosure.id == association_table.c.enclosure_id',
    #    secondaryjoin='Zoo.id == association_table.c.zoo_id',
    #    back_populates='enclosures')
    
    #enclosures = db.Relationship("Zoo", back_populates='enclosures')
    zoos = db.relationship(
        "Zoo",
        secondary=zoo_enclosure,
        back_populates="enclosures"
    )

class EnclosureSchema(ma.Schema):
    name = String(required=True)

    animal = fields.Nested('AnimalSchema', many=True)
    zoos = fields.Nested('ZooSchema', many=True)  # Serialize related zoos

    class Meta:
        fields = ('id', 'price', 'species', 'name', 'zoos')
one_enclosure = EnclosureSchema()

many_enclosures = EnclosureSchema(many=True, exclude=['zoos'])
enclosure_without_id = EnclosureSchema(exclude=['id'])