from init import db


zoo_enclosure = db.Table(
    'zoo_enclosure',
    db.Column('zoo_id', db.Integer, db.ForeignKey('zoos.id'), primary_key=True),
    db.Column('enclosure_id', db.Integer, db.ForeignKey('enclosures.id'), primary_key=True)
)