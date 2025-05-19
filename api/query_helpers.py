""" SQLAchemy Query helpers """

from sqlalchemy.orm import session
from sqlalchemy.orm import joinedload
from typing import Optional
from models import Movie, Link, Rating, Tag


# --- Mouvies ---

def get_movie(db: session, movie_id: int):
    """ Recupere un film par son ID """
    return db.query(Movie).filter(Movie.movieId == movie_id).first()

def get_movies(db: session, skip: int = 0, limit: int = 100, title: str = None, genre: str = None):
    """ Reccupere une liste de transaction avec filtre optionel """
    query = db.query(Movie)
    if (title):
        query = query.filter(Movie.title.like(f"%{title}%"))
    if genre:
        query = query.filter(Movie.genre.like(f"%{genre}%"))

    return query.offset(skip).limit(limit).all()

# --- Ratings ---

def get_rating(db: session, user_id: int, movie_id: int):
    """ Recupere un rating par le couple (userId et movieId) """
    return db.query(Rating).filter(Rating.userId == user_id and Rating.movieId == movie_id).first()

def get_ratings(db: session, skip: int = 0, limit: int = 100, user_id: int = None, movie_id: int = None, min_rate: float = None):
    """ Reccupere une liste de rating avec filtre optionel """
    query = db.query(Rating)
    if (user_id):
        query = query.filter(Rating.userId == user_id)
    if movie_id:
        query = query.filter(Rating.movieId == movie_id)
    if min_rate:
        query.filter(Rating.rate >= min_rate)

    return query.offset(skip).limit(limit).all()

def get_tag(db: session, user_id: int, movie_id: int, tag_test: str):
    """ Reccupere un tag en fonction des champs userId, movieId et tag_text """
    return(
        db.query(Tag)
        .filter(
            Tag.movieId == movie_id,
            Tag.userId == user_id,
            Tag.tag == tag_test
        )
        .first()
    )
   
def get_tags(
        db: session, 
        skip: int = 0, 
        limit: int =100, 
        user_id: int = None, 
        movie_id: int = None):
    query = db.query(Tag)
    if user_id:
        query.filter(Tag.userId == user_id)
    if movie_id:
        query.filter(Tag.movieId == movie_id)
    return query.offset(skip).limit(limit).all()

# --- Links ---
def get_link(db: session, movie_id):
    """ Recupere les IMDB ET TMDB associe a un film donnees """
    return db.query(Link).filter(Tag.movieId == movie_id).first()

def get_links(db: session, skip: int = 0, limit: int = 100):
    return db.query(Tag).offset(skip).limit(limit).all()

# --- Requetes analytiques ---
def get_movie_count(db: session):
    """ Retourne le nombre de film """
    return db.query(Movie).count()
def get_rating_count(db: session):
    """ Retourne le nombre de Rating """
    return db.query(Rating).count()
def get_tag_count(db: session):
    """ Retourne le nombre de tag """
    return db.query(Tag).count()
def get_link_count(db: session):
    """ Retourne le nombre de link """
    return db.query(Link).count()
