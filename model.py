"""Model and database functions for Craigslist searcher."""

from flask_sqlalchemy import SQLAlchemy
from flask import session

db = SQLAlchemy()

######### Model definitions #########

class Posting(db.Model):
    """Each object represents a Craigslist apartment post."""

    __tablename__ = "postings"

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.Integer)
    url = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Post: %s price: %s bedrooms: %s>" % (self.post_id, self.price, self.bedrooms)

    # TODO: Wrap class methods into one 'get apartments' function.

    @classmethod
    def get_lat_lons(cls, max_rent, num_rooms):
        """
        Given price and # of bedrooms, return list of matching apartment objects.
        """

        # First, retrieve list of ids, latitudes, and longitudes of apts
        # with desired number of bedrooms and within budget.
        query = db.session.query(cls.post_id, cls.latitude, cls.longitude).filter(cls.price < max_rent, cls.bedrooms == num_rooms)

        all_lat_lons = query.all()

        return all_lat_lons

    @classmethod
    def calculate_distance():
        # Then, calculate distance from origin to each apartment.
        # If apartment is within desired range, retrieve that object and add to list.
        matching_apts = []
        for post_id, lat, lon in all_lat_lons:
            # Calculate Euclidean distance
            distance_deg = math.sqrt((lat - session['origin_latitude'])**2 + (lon - session['origin_longitude'])**2)
            distance_mi = distance_deg * 69
            if distance_deg < session['max_distance']:
                matching_apts.append(Posting.query.get(post_id))

        return matching_apts

######### Helper Functions #########

def connect_to_db(app):
    """Connect database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cl.db'
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    """Allow us to interact with database when run in interactive mode."""

    from server import app
    connect_to_db(app)
    print "Connected to db."
