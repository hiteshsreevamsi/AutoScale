from sqlalchemy_serializer.serializer import SerializerMixin

from . import db


class ZipInfo(db.Model, SerializerMixin):
    __tablename__ = 'ZIPINFO'

    serialize_only = "state", "city", "zip"

    zip = db.Column(db.String, primary_key=True)
    lat = db.Column(db.Float(precision=64))
    long = db.Column(db.Float(precision=64))
    city = db.Column(db.String, default="")
    state = db.Column(db.String, default="")

    def __init__(self, *args, **kwargs):
        super(ZipInfo, self).__init__(*args, **kwargs)
