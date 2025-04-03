from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow.fields import String, Date
from models.association import zoo_enclosure
class Zoo(db.Model):
    __tablename__ = 'zoos'
    id = db.Column(db.Integer, primary_key=True)

    city = db.Column(db.String(100), nullable=False)
    weather = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(250))
    # many to one

    #enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'), nullable=False)

    #enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'), nullable=False, unique=False)
    #enclosures = db.Relationship("Enclosure", secondary='enclosures', back_populates = "enclosures")
    # testing 
    #association_table = db.Table(
    #'association_table',
    #db.metadata,
   # db.Column('zoo_id', db.Integer, db.ForeignKey('zoos.id')),
   # db.Column('enclosure_id', db.Integer, db.ForeignKey('enclosures.id'))
#


    

    #zoo_id = db.Column(db.Integer, db.ForeignKey('zoos.id'), nullable=False, unique=False)
    #enclosures = db.Relationship(
     #   'Enclosure',
     #   secondary='association_table',
      #  primaryjoin='Zoo.id == association_table.c.zoo_id',
      #  secondaryjoin='Enclosure.id == association_table.c.enclosure_id',
       # back_populates='zoos'

    #)
 
    enclosures = db.Relationship('Enclosure', secondary=zoo_enclosure, back_populates='zoos')

    #enclosure_table = db.Table("enclosures",
     #   db.Column("enclosure_id", db.Integer, db.ForeignKey('enclosures.id')),
     #   db.Column("zoo_id", db.Integer, db.ForeignKey('zoos.id'))                           
    #)
    
    #enclosures = db.Relationship("Zoo", secondary=enclosure_table, backref = 'zoos')

    # lets try this
class ZooSchema(ma.Schema):
    enclosures = fields.Nested('EnclosureSchema', many=True, exclude=['zoos'])  # Serialize related enclosures
    class Meta:
        fields = ('id', 'city', 'weather', 'name', 'enclosures')


one_zoo = ZooSchema()

many_zoos = ZooSchema(many=True)
zoo_without_id = ZooSchema(exclude=['id'])