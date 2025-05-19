from pydantic import BaseModel
from typing import Optional, List

# ----  schemas secondaire  -----

class RatingBase(BaseModel):
    userId: int
    movieId: int
    rate: float
    timestamp: int

    class config:
        orm_mode = True

class TagBase(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int

    class config:
        orm_mode = True

class LinkBase(BaseModel):
    imdbId: Optional[str]
    tmdId: Optional[str]

    class config:
        orm_mode = True

# ----  Schema principal pour movies    ----

class MovieBase(BaseModel):
    movieId: int
    title: str
    genre: Optional[str] = None

    class config:
        orm_mode = True


class MovieDetailed(MovieBase):
    ratings: list[RatingBase]
    tags: list[TagBase]
    link: Optional[LinkBase] = None


# ----  Schemas pour liste de films (sans details imbriques)    ----

class MovieSimple(BaseModel):
    movieId: int
    title: str
    genre: Optional[str]

    class config:
        orm_mode = True


# ----- Pour les endpoints de /ratings et / Tages si appeles seuls  -----

class RatingSimple(BaseModel):
    userId: int
    movieId: int
    rate: float
    timestamp: int

    class config:
        orm_mode = True

class TagSimple(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int

    class config:
        orm_mode = True

class LinkSimple(BaseModel):
    movieId: int
    imdbId: Optional[str]
    tmdId: Optional[str]

    class config:
        orm_mode = True


    
