from fastapi import FastAPI, HTTPException, status
from pymongo import MongoClient
from neo4j import GraphDatabase
from dotenv import dotenv_values
from routes import router as movies_router

# Chargement de la configuration depuis le fichier .env
config = dotenv_values(".env")

# Initialisation de l'application FastAPI
app = FastAPI()

@app.on_event("startup")
def initialize_databases():
    # Connexion à MongoDB avec l'URI du fichier .env
    app.mongodb_client = MongoClient(config["MONGO_URI"])
    app.database = app.mongodb_client[config["DB_NAME_M"]]

    # Connexion à Neo4j avec les informations d'identification du fichier .env
    neo4j_uri = config['NEO4J_URI']
    neo4j_user = config['NEO4J_USER']
    neo4j_password = config['NEO4J_PASSWORD']
    app.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

@app.get("/")
async def root():
    # Point d'accès simple pour vérifier si l'API fonctionne
    return {"message": "Final Lab - MongoDB & Neo4j"}

def fetch_mongodb_movie_titles():
    # Récupération des titres des films de la collection 'movies', en excluant le champ '_id'
    movies = app.database["movies"].find({}, {"title": 1, "_id": 0})
    return {movie["title"] for movie in movies if "title" in movie}

def fetch_neo4j_movie_titles():
    query = "MATCH (m:Movie) RETURN m.title AS title"
    with app.neo4j_driver.session() as session:
        result = session.run(query)
        return {record["title"] for record in result}

@movies_router.get("/common_movies", response_description="Nombre de films communs entre MongoDB et Neo4j", tags=["MongoDB & Neo4j"])
def get_common_movies():
    try:
        mongodb_titles = fetch_mongodb_movie_titles()
        neo4j_titles = fetch_neo4j_movie_titles()
        common_titles = mongodb_titles.intersection(neo4j_titles)
        return {"common_movies_count": len(common_titles), "titles": list(common_titles)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def fetch_people_who_rated_movie(movie_title: str):
    query = """
    MATCH (u:Person)-[r:REVIEWED]->(m:Movie {title: $title})
    RETURN u.name AS user_name
    """
    with app.neo4j_driver.session() as session:
        result = session.run(query, title=movie_title)
        return [record["user_name"] for record in result]

@movies_router.get("/reviewers-who-rated", response_description="Liste des utilisateurs ayant évalué un film spécifique", tags=["Neo4j"])
def get_reviewers_for_movie(title: str):
    try:
        users = fetch_people_who_rated_movie(title)
        if users:
            return {"users": users}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucun utilisateur n'a évalué le film '{title}'")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def fetch_reviewer_details(user_name: str):
    query = """
    MATCH (u:Person {name: $name})-[r:REVIEWED]->(m:Movie)
    RETURN u.name AS user_name, count(m) AS rated_movies_count, collect(m.title) AS rated_movies
    """
    with app.neo4j_driver.session() as session:
        result = session.run(query, name=user_name)
        record = result.single()
        if record:
            return {
                "user_name": record["user_name"],
                "rated_movies_count": record["rated_movies_count"],
                "rated_movies": record["rated_movies"]
            }
        return None

@movies_router.get("/reviewers-ratings", response_description="Détails des utilisateurs avec le nombre de films évalués et la liste des films", tags=["Neo4j"])
def get_reviewer_details(name: str):
    try:
        user_details = fetch_reviewer_details(name)
        if user_details:
            return user_details
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Utilisateur '{name}' non trouvé")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

app.include_router(movies_router, prefix="/movies")

@app.on_event("shutdown")
def close_databases():
    app.mongodb_client.close()
    app.neo4j_driver.close()
