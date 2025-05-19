"""Database configuration!!"""

from sqlite3 import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///./movies.db"

# Creation d'un moteur (engine) de bd permettant d'etablir une connexion avec notre bd sqlite (movies.db)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Definir une session local, qui permet de creer des sessions pour interagir avec la base de donnees

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine)

# Definir base que servira de class de base pour notre model alchemy
Base = declarative_base()

if __name__=="__main__":
    try:
        with engine.connect() as conn:
            print("Connection a la base donnees reussie avec succes")
    
    except Exception as e:
        print(f"Erreur de connexion a la base de donnees {e}")
