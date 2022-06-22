from flask import request
from flask_restx import Resource, Namespace
from app.schemas import MovieSchema
from app.models import db, Movie, Genre, Director
from app.utils import get_query, pagination

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        """
        Возвращает список всех фильмов, разделенный по страницам; фильмы определенного режиссера;
        фильмы определенного жанра; фильмы определенного режиссера и жанра
        """
        movies_query = get_query()
        director_id = request.args.get('director_id', type=int)
        if director_id:
            movies_query = movies_query.filter(Movie.director_id == director_id)
        genre_id = request.args.get('genre_id', type=int)
        if genre_id:
            movies_query = movies_query.filter(Movie.genre_id == genre_id)
        else:
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 10))
            movies_query = pagination(movies_query, page, page_size).all()
        return movies_schema.dump(movies_query), 200

    def post(self):
        """
        Добавляет кино в фильмотеку
        """
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
            db.session.commit()
        return "Новый фильм добавлен в базу", 201


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        """
        Возвращает подробную информацию о фильме по его id
        """
        try:
            movie = db.session.query(Movie.id, Movie.title,
                Movie.description, Movie.trailer,
                Movie.year, Movie.rating,
                Genre.name.label('genre'),
                Director.name.label('director')).join(Genre).join(Director).filter(Movie.id == mid).first()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return e, 404

    def put(self, mid):
        """
        Обновляет кино по id
        """
        movie = db.session.query(Movie).get(mid)
        if not movie:
            return "Фильма с таким id нет", 404
        req_json = request.json
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()
        return "Данные обновлены", 204

    def delete(self, mid: int):
        """
         Удаляет фильм по id
        """
        movie = db.session.query(Movie).get(mid)
        if not movie:
            return "Фильма с таким id нет", 404
        db.session.delete(movie)
        db.session.commit()
        return "", 204
