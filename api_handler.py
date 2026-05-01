import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w200"

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}


def search_movies(query: str) -> list:
    """Search movies by title. Returns list of movie dicts."""
    url = f"{BASE_URL}/search/movie"
    params = {"query": query, "language": "en-US", "page": 1}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.ConnectionError:
        print("Error: No internet connection.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return []


def get_movie_details(movie_id: int) -> dict:
    """Get full details of a movie by ID."""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"language": "en-US"}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details: {e}")
        return {}


def get_poster_url(poster_path: str) -> str:
    """Build full poster image URL."""
    if poster_path:
        return f"{IMAGE_BASE_URL}{poster_path}"
    return ""