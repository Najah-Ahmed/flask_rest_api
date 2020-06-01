from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Movies(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    movie_name = db.Column(db.String(100), unique=True)
    movie_bio = db.Column(db.String(500))

    def __init__(self, public_id,  movie_name,  movie_bio):
        self.public_id = public_id
        self.movie_name = movie_name
        self.movie_bio = movie_bio


class MovieSchema(ma.Schema):
    class Meta:
        fields = ('movie_id', 'public_id', 'movie_name', 'movie_bio')


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@app.route('/movies', methods=['POST'])
def add_movie():
    movie_name = request.json['name']
    movie_bio = request.json['bio']
    public_id = str(uuid.uuid4())
    new_movie = Movies(public_id,  movie_name,  movie_bio)
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({"message": "movie Created"}), 201


@app.route('/movies', methods=['GET'])
def get_all_movies():
    all_movies = Movies.query.all()
    result = movies_schema.dump(all_movies)
    return jsonify(result)


@app.route('/movies/<string:public_id>', methods=['GET'])
def get_movies(public_id):
    movie = Movies.query.filter_by(public_id=public_id).first()
    return movie_schema.jsonify(movie)


@app.route('/movies/<string:public_id>', methods=['PUT'])
def update_movies(public_id):
    movie = Movies.query.filter_by(public_id=public_id).first()
    if not movie:
        return jsonify({"message": "Not found Movie"})

    movie_name = request.json['name']
    movie_bio = request.json['bio']

    movie.movie_name = movie_name
    movie.movie_bio = movie_bio
    db.session.commit()

    return jsonify({"message": "Update Movie"}), 201


@app.route('/movies/<string:public_id>', methods=['DELETE'])
def delete_movies(public_id):
    movie = Movies.query.filter_by(public_id=public_id).first()
    if not movie:
        return jsonify({"message": "Not found Movie"})
    else:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"message": "Deleted Movie"}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)
