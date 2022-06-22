from flask import request
from flask_restx import Resource, Namespace
from app.schemas import GenreSchema
from app.models import db, Genre

genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        """
        Возвращает все жанры
        """
        all_genres = db.session.query(Genre).all()
        return genres_schema.dump(all_genres), 200

    def post(self):
        """
        Добавляет жанр
        """
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
            db.session.commit()
        return "Новый жанр добавлен в базу", 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        """
        Возвращает жанр по его id
        """
        genre = db.session.query(Genre).get(gid)
        if genre:
            return genre_schema.dump(genre), 200
        return "Жанра с таким id нет", 404

    def put(self, gid):
        """
        Обновляет жанр по id
        """
        genre = db.session.query(Genre).get(gid)
        if not genre:
            return "Жанра с таким id нет", 404
        req_json = request.json
        genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()
        return "Данные обновлены", 204

    def delete(self, gid: int):
        """
        Удаляет жанр
        """
        genre = db.session.query(Genre).get(gid)
        if genre is None:
            return "Жанра с таким id нет", 404
        db.session.delete(genre)
        db.session.commit()
        return "", 204
