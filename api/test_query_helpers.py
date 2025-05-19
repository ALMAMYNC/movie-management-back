from database import SessionLocal
from query_helpers import *

db = SessionLocal()

movie = get_movie(db, 1)
print(movie.title, movie.genre)

db.close()