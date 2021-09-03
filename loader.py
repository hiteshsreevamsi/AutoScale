import os

import pandas as pd
from sqlalchemy.exc import IntegrityError

from models import db
from models.dealers import Dealers
from models.listings import Listings
from models.zip_info import ZipInfo

PAR_DIR = os.path.join(os.path.abspath(os.curdir), "data")

data_dealers = pd.read_csv(os.path.join(PAR_DIR, "dealers.csv"), encoding_errors="ignore")
data_dealers.rename(columns={"dealer_address_1": "dealer_address"}, inplace=True)
data_dealers.fillna("", inplace=True)
data_listings = pd.read_csv(os.path.join(PAR_DIR, "listings.csv"), encoding_errors="ignore")
data_zip = pd.read_csv(os.path.join(PAR_DIR, "zip_info.csv"), usecols=[0, 1, 2, 3, 4], header=None,
                       encoding_errors="ignore")
data_zip.columns = ["zip", "state", "lat", "long", "city"]


def load_data():
    print("Loading Data")
    for i, dealer in data_dealers.iterrows():
        if db.session.query(Dealers.dealer_number).filter_by(dealer_number=dealer.dealer_number).first():
            continue
        db.session.add(Dealers(**dealer))
    try:
        db.session.commit()
    except IntegrityError:
        pass


def load_listings():
    print("Loading Listings")
    cols_in_scope = Listings.__table__.columns.keys()
    for i, temp_store in data_listings.iterrows():
        if db.session.query(Listings.vehicle_live_id).filter_by(vehicle_live_id=temp_store.vehicle_live_id).first():
            continue
        db.session.add(Listings(**temp_store[cols_in_scope]))
    try:
        db.session.commit()
    except IntegrityError:
        pass


def load_zip():
    print("Loading Zip")
    for i, zip_data in data_zip.iterrows():
        if db.session.query(ZipInfo.zip).filter_by(zip=zip_data.zip).first():
            continue
        db.session.add(ZipInfo(**zip_data))
    try:
        db.session.commit()
    except IntegrityError:
        pass


def load_all():
    load_zip()
    load_listings()
    load_data()
