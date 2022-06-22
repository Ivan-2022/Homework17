from flask import request
from flask_restx import Resource, Namespace
from app.schemas import DirectorSchema
from app.models import db, Director

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        """
        Возвращает всех режиссеров
        """
        all_directors = db.session.query(Director).all()
        return directors_schema.dump(all_directors), 200

    def post(self):
        """
        Добавляет режиссера
        """
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
            db.session.commit()
        return "Новый режиссер добавлен в базу", 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        """
        Возвращает режиссера по его id
        """
        director = db.session.query(Director).get(did)
        if director:
            return director_schema.dump(director), 200
        return "Режиссера с таким id нет", 404

    def put(self, did):
        """
        Обновляет режиссера
        """
        director = db.session.query(Director).get(did)
        if not director:
            return "Режиссера с таким id нет", 404
        req_json = request.json
        director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()
        return "Данные обновлены", 204

    def delete(self, did: int):
        """
        Удаляет режиссера
        """
        director = db.session.query(Director).get(did)
        if director is None:
            return "Режиссера с таким id нет", 404
        db.session.delete(director)
        db.session.commit()
        return "", 204
