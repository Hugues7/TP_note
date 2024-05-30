from fastapi import APIRouter, Body, Request, HTTPException, status, Query
from typing import List, Optional
from models import Movie, MovieUpdate

# Create the router
router = APIRouter()

@router.get("/", response_description="List all movies [MongoDB]", response_model=List[Movie], tags=["MongoDB"])
def list_all_movies(request: Request):
    """
    Retrieve and return a list of the first 6 movies from the MongoDB collection.
    """
    movies = list(request.app.database["movies"].find({}, {"_id": 0}).limit(6))
    return movies

@router.get("/search", response_description="Search movies by title or actor", response_model=List[Movie], tags=["MongoDB"])
def search_movies(request: Request, title: Optional[str] = Query(None), actor: Optional[str] = Query(None)):
    """
    Search for movies in the MongoDB collection by title or actor name.
    If no parameters are provided, return all movies.
    """
    query = {}
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if actor:
        query["cast"] = {"$regex": actor, "$options": "i"}

    movies = list(request.app.database["movies"].find(query, {"_id": 0}))

    if movies:
        return movies

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found with the given criteria")

@router.put("/update", response_description="Update movie information", response_model=Movie, tags=["MongoDB"])
def update_movie(title: str, request: Request, movie: MovieUpdate = Body(...)):
    """
    Update specific information for a movie in the MongoDB collection by its title.
    """
    movie_data = {k: v for k, v in movie.dict().items() if v is not None}

    if movie_data:
        update_result = request.app.database["movies"].update_one({"title": title}, {"$set": movie_data})

        if update_result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title '{title}' not found")

    updated_movie = request.app.database["movies"].find_one({"title": title}, {"_id": 0})

    if updated_movie:
        return updated_movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title '{title}' not found")
