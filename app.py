import os
import time

import flask
import numpy as np
from flask import jsonify
from flask.json import JSONEncoder
from sqlalchemy.engine.row import Row

from distance import reachable_zip_code
from loader import load_all
from models import db
from models.dealers import Dealers
from models.listings import Listings
from models.zip_info import ZipInfo


class CustomEncoder(JSONEncoder):
    def default(self, o):
        if issubclass(o.__class__, db.Model):
            return o.to_dict()
        if issubclass(o.__class__, Row):
            return dict(o)
        return JSONEncoder.default(self, o)


app = flask.Flask(__name__, static_url_path='')
app.secret_key = "some-random-secret-key"
base_directory = path = os.path.dirname(os.path.realpath(__file__))
app.json_encoder = CustomEncoder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_directory, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    if flask.request.method == "GET":
        return flask.render_template("home.html")
    else:
        data = flask.request.form
        filtered_data = search(data["search_query"], data["radius"])["cars"]
        if not filtered_data:
            flask.flash("Zip code not found!", "error")
            return flask.redirect(flask.url_for("home"))

        filtered_data = [{**d["Listings"].to_dict(), **d["Dealers"].to_dict(), **d["ZipInfo"].to_dict()}
                         for d in
                         filtered_data]
        return flask.render_template("content.html",
                                     data=filtered_data, keys=filtered_data[0].keys())


@app.route("/dealers", methods=["GET"])
def dealers():
    return jsonify(dealers=Dealers.query.all())


@app.route("/search/<zipcode>/<miles>", methods=["GET"])
def search(zipcode, miles):
    start_time = time.time()
    zipcodeObject = ZipInfo.query.filter_by(zip=zipcode).first()
    if not zipcodeObject:
        return dict(cars=[])
    reachablezipCodes = ZipInfo.query.all()
    zips = np.array([i.zip for i in reachablezipCodes])
    mask = reachable_zip_code([i.lat for i in reachablezipCodes], [i.long for i in reachablezipCodes],
                              zipcodeObject.lat,
                              zipcodeObject.long, int(miles))
    cars = Listings.query \
        .join(Dealers, Dealers.dealer_number == Listings.dealer_number) \
        .add_columns(Dealers) \
        .filter(Listings.zip.in_(zips[mask])) \
        .join(ZipInfo, ZipInfo.zip == Listings.zip) \
        .add_column(ZipInfo) \
        .all()
    print("duration: ", (time.time() - start_time))
    return dict(cars=cars)


@app.route("/load_data", methods=["GET"])
def load_data_into_db():
    load_all()
    return ""


if __name__ == "__main__":
    app.run(host="localhost")
