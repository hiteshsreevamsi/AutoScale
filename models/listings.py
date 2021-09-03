from sqlalchemy_serializer.serializer import SerializerMixin

from . import db


class Listings(db.Model, SerializerMixin):
    __tablename__ = "LISTINGS"

    serialize_only = "year", "make", "model", "price"

    vehicle_live_id = db.Column(db.Integer, primary_key=True)
    dealer_number = db.Column(db.Integer, db.ForeignKey('DEALERS.dealer_number'))
    year = db.Column(db.Integer, default=0)
    amenities = db.Column(db.String, default="")
    vin = db.Column(db.String, default="")
    stock = db.Column(db.String, default="")
    make = db.Column(db.String, default="")
    model = db.Column(db.String, default="")
    trim = db.Column(db.String, default="")
    price = db.Column(db.Integer, default="")
    miles = db.Column(db.Integer, default="")
    exterior = db.Column(db.Integer, default="")
    description = db.Column(db.Integer, default="")
    certified = db.Column(db.Boolean, default=False)
    transmission = db.Column(db.String, default="")
    body_type = db.Column(db.String, default="")
    doors = db.Column(db.Integer, default=0)
    cylinders = db.Column(db.Integer, default=0)
    engine = db.Column(db.String, default="")
    displacement = db.Column(db.Integer, default=0)
    zip = db.Column(db.String, default="")
    imagefile = db.Column(db.String, default="")

    def __init__(self, *args, **kwargs):
        super(Listings, self).__init__(*args, **kwargs)
