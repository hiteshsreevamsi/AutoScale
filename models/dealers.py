from sqlalchemy_serializer.serializer import SerializerMixin

from . import db


class Dealers(db.Model, SerializerMixin):
    __tablename__ = 'DEALERS'

    serialize_only = "dealer_name",

    dealer_name = db.Column(db.String, default="")
    dealer_number = db.Column(db.Integer, primary_key=True)
    dealer_address = db.Column(db.String, default="")

    def __init__(self, *args, **kwargs):
        super(Dealers, self).__init__(*args, **kwargs)
