from movies import db


class Movies(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False, unique=True)
    year = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Float(), nullable=True)
    ranking = db.Column(db.Integer(), nullable=True)
    review = db.Column(db.String(), nullable=True)
    img_url = db.Column(db.String(), nullable=False)
