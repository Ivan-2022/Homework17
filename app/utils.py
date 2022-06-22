from app.models import db, Movie, Director, Genre


def get_query():
    movies_query = db.session.query(Movie.id, Movie.title,
                    Movie.description, Movie.trailer,
                    Movie.year, Movie.rating,
                    Genre.name.label('genre'),
                    Director.name.label('director')).join(Genre).join(Director)
    return movies_query


def pagination(query, page, page_size):
    return query.limit(page_size).offset((page - 1) * page_size)
