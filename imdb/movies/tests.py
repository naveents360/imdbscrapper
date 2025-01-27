import pytest
from rest_framework.test import APIClient
from .models import Movie  

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imdb.settings')
django.setup()


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """Fixture to provide an API client for testing."""
    return APIClient()


@pytest.fixture
def create_movies():
    """Fixture to create sample movie data."""
    Movie.objects.create(title="Comedy Movie 1", genre="comedy", year=2021, rating=7.5)
    Movie.objects.create(title="Comedy Movie 2", genre="comedy", year=2022, rating=8.0)
    Movie.objects.create(title="Drama Movie", genre="drama", year=2020, rating=7.0)


def test_movie_search_comedy(api_client, create_movies):
    """Test the movie search API for 'comedy'."""
    response = api_client.get("/api/movies/?search=comedy")

    assert response.status_code == 200
    
    data = response.json()
    data = data['results']
    assert len(data) == 2 
    assert data[0]["genre"] == "comedy"
    assert data[1]["genre"] == "comedy"

def test_movie_search_drama(api_client, create_movies):
    """Test the movie search API for 'comedy'."""
    response = api_client.get("/api/movies/?search=drama")

    assert response.status_code == 200
    
    data = response.json()
    data = data['results']
    assert len(data) == 1
