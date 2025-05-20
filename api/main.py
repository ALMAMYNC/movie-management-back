from fastapi import FastAPI, Depends, HTTPException, Query, Path
import schemas_pydantic
import query_helpers as helpers
from sqlalchemy.orm import session
from database import SessionLocal
from typing import Optional, List

# ---- Initialisation de l'api ------

movie_description = """ Bienvenue dans MovieLens """
app = FastAPI(
    title= "MovieLens API",
    description= movie_description,
    version= "0.1",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---- Definitiond de quelques routes

# endpoint pour tester la sante l'api

@app.get(
    "/",
    summary="Verification si l'api fonctionne",
    description="Ferivier si l'api fonctionne bien",
    operation_id= "movie_api_health_checking",
    tags=["Monitoring"]
)

async def root():
    return {
        "message": "l'API est maintenant operationnel"
    }

@app.get(
    "/movies/{movie_id}",
    summary="Obtenir un movie par son ID",
    description="Cet endpoint renvoi un film a l'aide de son endpoint",
    response_description= "Les details d'un film",
    response_model= schemas_pydantic.MovieDetailed,
    tags=["movies"]
)

async def read_movie(movie_id: int = Path(..., description= "L'identifiant unique du film"), db:session= Depends(get_db)):
    movie = helpers.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"film avec l'ID {movie_id} n'a pas ete trouve")
    return movie


#  --- Endpoint pour obtenir une liste des films (avec pagination et filtres facultatifs titre, genre, skip et limit)

@app.get(
    "/movies",
    summary="Liste des films",
    description= "Retourne une liste de films avec pagination et filtres optionnels par titre ou genre",
    response_description="Liste des films",
    response_model=list[schemas_pydantic.MovieSimple],
    tags= ["films"]
)
async def list_movies(
    skip: int = Query(0, ge= 0, description="Nombre de resultat a ignorer"),
    limit: int = Query(100, le=1000, description="Nombre de resultats a retourner"),
    title: str = Query(None, description="Filtre a partir du titre"),
    genre: str = Query(None, description="Filtre par genre"),
    db: session = Depends(get_db)
):
    movies = helpers.get_movies(db, skip = skip, limit = limit, title = title, genre = genre)
    if movies is None:
        raise HTTPException(status_code= 404, detail="Liste de films non trouve")
    return movies


# Endpoint pour obtenir une evaluation par utilisateur et film

@app.get(
    "/ratings/{user_id}/{movie_id}",
    summary="Obtenir une evelation par utilisateur et film",
    description= "Retourne l'evaluation d'un utilisateur pour un film donne",
    response_description="Detail de l'evaluation",
    response_model=schemas_pydantic.RatingSimple,
    tags= ["evaluation"]
)
async def read_rating(
    user_id: int = Path(..., description="ID de l'utilisateur"),
    movie_id: int = Path(..., description="ID du film"),
    db: session = Depends(get_db)
):
    rating = helpers.get_rating(db, user_id= user_id, movie_id= movie_id)
    if rating is None:
        raise HTTPException(status_code= 404, detail="L'evaluation non trouvee")
    return rating

# Endpoint pour obtenir une liste d'evaluation avec filtre par utilisateur ou par film avec pagination

@app.get(
    "/ratings",
    summary="Obtenir une liste d'evelation par utilisateur ou par film",
    description= "Retourne une liste d'evaluation avec filtre par utilisateur ou par film donne",
    response_description="Liste d'evaluation",
    response_model=list[schemas_pydantic.RatingSimple],
    tags= ["evaluation"]
)
async def list_rating(
    skip: int = Query(0, ge=0, description="Nombre de rating"),
    limit: int = Query(100, le=1000, description="Nombre maximum de resultat a retourner"),
    user_id: int = Query(None, description="ID de l'utilisateur"),
    movie_id: int = Query(None, description="ID du film"),
    min_rate: float = Query(None,ge=0.0, le=5.0, description="Filtrer les notes superieurs ou egales a cette valeur"),
    db: session = Depends(get_db)
):
    rating = helpers.get_ratings(db, skip= skip, limit= limit, user_id= user_id, movie_id= movie_id, min_rate= min_rate)
    if rating is None:
        raise HTTPException(status_code= 404, detail="Aucune liste trouve")
    return rating


# Endpoint pour obtenir un tag a l'aide d'id de l'utilisateur, l'id du film et le tag

@app.get(
    "/tags/{user_id}/{movie_id}/{tag_text}",
    summary="Obtenir un tag a partir l'id de l'utilisateur, l'id du film et le text du tag",
    description="Retourne le tag en fonction de l'id de l'utilisateur et du filme et le text du tag",
    response_description="Les detail d'un tag",
    response_model=schemas_pydantic.TagSimple,
    tags=["Tags"]
)
async def read_tag(
    user_id: int = Path(..., description="ID de l'utilisateur"),
    movie_id: int = Path(..., description="ID du films"),
    tag_text: str = Path(..., description="Le text du tag"),
    db: session = Depends(get_db)
):
    tag = helpers.get_tag(
        db,
        user_id=user_id,
        movie_id= movie_id,
        tag_text= tag_text
    )
    if tag is None:
        raise HTTPException(status_code=404, detail="Aucun tag trouve")
    return tag


# Endpoint pour obtenir les tags avec filtre par utilisateur ou par film

@app.get(
    "/tags",
    summary="Obtenir une liste de tag avec filtre par utilisateur et par film",
    description="Retourne une liste de tag en filtrant par utilisateur et par film",
    response_description="Liste de tags",
    response_model=list[schemas_pydantic.TagSimple],
    tags=["Tags"]
)
async def liste_tags(
    skip: int = Query(0, ge=0, description="Le nombre de tag a ignorer"),
    limit: int = Query(10, le=100, description="Le nombre maximum de tag a retourner"),
    user_id: int = Query(None, description="Id de l'utilisateur"),
    movie_id: int = Query(None, description="L'id du film"),
    db: session = Depends(get_db)
):
    list_tags = helpers.get_tags(
        db,
        skip= skip,
        limit= limit,
        user_id= user_id,
        movie_id= movie_id
    )
    if list_tags is None:
        raise HTTPException(status_code= 404, detail="Aucune liste trouve")
    return list_tags

# Endpoint pour obtenir IMDB et TMDB associe a un film donnee

@app.get(
    "/links/{movie_id}",
    summary="Obtenir IMDB et TMDB associe a un film donnee",
    description="Retourne l'IMDB et TMDB associe a film donne",
    response_description="Le lien",
    response_model=schemas_pydantic.LinkSimple,
    tags=["Links"]
)
async def read_link(
    movie_id: int = Path(..., description="ID du films"),
    db: session = Depends(get_db)
):
    link = helpers.get_link(
        db,
        movie_id= movie_id,
    )
    if link is None:
        raise HTTPException(status_code=404, detail="Aucun tag trouve")
    return link

# Endpoint pour obtenir les liens par pagination

@app.get(
    "/links",
    summary="Obtenir les liens par pagination",
    description="Retourne une liste de liens avec pagination",
    response_description="Les liens pagines",
    response_model=list[schemas_pydantic.LinkSimple],
    tags=["Links"]
)
async def liste_links(
    skip: int = Query(0, ge=0, description="Le nombre de lien a ignorer"),
    limit: int = Query(10, le=100, description="Le nombre maximum de liens a retourner"),
    db: session = Depends(get_db)
):
    list_links = helpers.get_links(
        db,
        skip= skip,
        limit= limit
    )
    if list_links is None:
        raise HTTPException(status_code= 404, detail="Aucune liste trouve")
    return list_links

# Enpoints analytiques pour obtenir des statistiques sur a base de donnees
@app.get(
    "/analytics",
    summary="Obtenir le nombre total de films",
    description="""
    Retourne un resume des statistiques de la base de donnees
    
    """,
    response_description="Analyque",
    response_model= schemas_pydantic.AnalyticsResponse,
    tags=["Analytics"]
)
async def get_movie_count(db: session = Depends(get_db)):
    movie_count = helpers.get_movie_count(db)
    rating_count  = helpers.get_rating_count(db)
    tag_count = helpers.get_tag_count(db)
    link_count = helpers.get_link_count(db)

    return schemas_pydantic.AnalyticsResponse(
        movie_count= movie_count,
        rating_count= rating_count,
        tag_count= tag_count,
        link_count= link_count
    )

   

