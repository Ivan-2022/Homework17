from flask import Flask
from flask_restx import Api
from app.models import db
from app.views.movies import movie_ns
from app.views.directors import director_ns
from app.views.genres import genre_ns

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False}

api = Api(app)
api.add_namespace(movie_ns)
api.add_namespace(director_ns)
api.add_namespace(genre_ns)

app.app_context().push()
db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
