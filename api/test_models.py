# %% 
from database import SessionLocal
from models import Movie, Tag, Rating, Link

# %%
db = SessionLocal()
# %%
# movies = db.query(Movie).limit(5).all()
# for movie in movies:
#     print(f"ID: {movie.movieId} Title: {movie.title} Genre: {movie.genre}")
# else:
#     print("No data")
# %%
# action_movies = db.query(Movie).filter(Movie.genre.contains("Action")).limit(5).all()
# for movie in action_movies:
#     print(f"ID: {movie.movieId} Title: {movie.title} Genre: {movie.genre}")

# %%
# high_rated_movies = db.query(Movie).join(Rating).filter(Rating.rate >= 3.0).limit(5).all()

# for hrm in high_rated_movies.key:
#     print(hrm)

high = (
    db.query(Movie.title, Rating.rate)
    .join(Rating)
    .limit(5)
    .all()
)

for title, rate in high:
    print(title, rate)