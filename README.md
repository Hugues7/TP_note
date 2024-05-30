# Movie Database API

This is a FastAPI application that interacts with MongoDB and Neo4j databases to manage and query movie data and user reviews. The API provides endpoints to list movies, search for movies by title or actor, update movie information, and retrieve user reviews and ratings.

## Features

- List all movies from MongoDB.
- List specific movies based on the title or actor name from MongoDB.
- Update information about a specific movie in MongoDB.
- Return the number of common movies between MongoDB and Neo4j databases.
- List users who rated a movie in Neo4j.
- Return a user with the number of movies they have rated and the list of rated movies in Neo4j.

## Requirements

- Python 3.8+
- MongoDB
- Neo4j

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/moviedb-api.git
    cd moviedb-api
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**:

    Create a `.env` file in the root of the project and add the following variables:
    ```env
    MONGO_URI=mongodb://localhost:27017
    DB_NAME_M=movies_db
    NEO4J_URI=bolt://localhost:7687
    NEO4J_USER=neo4j
    NEO4J_PASSWORD=password
    ```

5. **Run the application**:
    ```bash
    uvicorn main:app --reload
    ```

## Usage

### List All Movies

- **Endpoint**: `GET /movies/`
- **Description**: Retrieve a list of the first 6 movies from the MongoDB collection.
- **Response**: A JSON array of movie objects.

### Search Movies by Title or Actor

- **Endpoint**: `GET /movies/search`
- **Description**: Search for movies by title or actor name. If no parameters are provided, return all movies.
- **Parameters**:
  - `title` (optional): The title of the movie.
  - `actor` (optional): The name of the actor.
- **Response**: A JSON array of movie objects matching the criteria.

### Update Movie Information

- **Endpoint**: `PUT /movies/update`
- **Description**: Update specific information for a movie in the MongoDB collection by its title.
- **Parameters**:
  - `title` (required): The title of the movie to be updated.
- **Body**: A JSON object with the fields to be updated.
- **Response**: The updated movie object.

### Get Common Movies Between MongoDB and Neo4j

- **Endpoint**: `GET /movies/common_movies`
- **Description**: Get the number of common movies between MongoDB and Neo4j databases.
- **Response**: A JSON object containing the count and list of common movie titles.

### List Users Who Rated a Movie

- **Endpoint**: `GET /movies/reviewers-who-rated`
- **Description**: Get users who rated a specific movie in Neo4j.
- **Parameters**:
  - `title` (required): The title of the movie.
- **Response**: A JSON array of user names who rated the movie.

### Get User Ratings and Reviewed Movies

- **Endpoint**: `GET /movies/reviewers-ratings`
- **Description**: Get a user with the number of movies they have rated and the list of rated movies in Neo4j.
- **Parameters**:
  - `name` (required): The name of the user.
- **Response**: A JSON object containing the user name, count of rated movies, and list of rated movie titles.

## Contributing

Contributions are welcome! Please create a pull request or submit an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License.
