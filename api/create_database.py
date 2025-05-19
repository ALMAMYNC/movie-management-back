from database import engine, Base
from models import Movie, Rating, Tag, Link

print("Creation de la base de donnees")
Base.metadata.create_all(bind=engine)
print("Base de donnees et tables crees avec success!")