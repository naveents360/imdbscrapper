from rest_framework.viewsets import ModelViewSet
from .models import Movie
from .serializers import MovieSerializer,GenreSerializer
import requests
from bs4 import BeautifulSoup
from rest_framework.response import Response
from rest_framework import status
import urllib.parse
import json
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logger = logging.getLogger('django')

def fetch_director_cast(data):
    logger.info("Making API Call to IMDB website to extract Director and Cast Details")
    extension = {
        "persistedQuery": {
        "sha256Hash": "28fdb27482f0852bc70811f36a5fab72e9afd1589b37c5e1aaecf438d418f6c7",
        "version": 1
        }
    }
    json_data = json.dumps(data)
    variables = urllib.parse.quote(json_data,safe=" ")
    variables = variables.replace(" ","")
    extension = json.dumps(extension)
    extension = urllib.parse.quote(extension,safe=" ")
    extension = extension.replace(" ","")    
    url = f"https://caching.graphql.imdb.com/?operationName=Title_Summary_Prompt_From_Base&variables={variables}&extensions={extension}"
    headers = {'Content-Type':'application/json'}
    resp = requests.get(url,headers=headers)
    if resp.status_code == 200:
        logger.info("API Call for IMDB is successfull")
        resp = resp.json()   
        cast = resp['data']['title']['principalCast'][0]['credits'] if len(resp['data']['title']['principalCast']) >0 else None
        cast = [ name['name']['nameText']['text'] for name in cast] if cast is not None else []
        director = resp['data']['title']['principalDirectors'][0]['credits'] if len(resp['data']['title']['principalDirectors']) >0 else None
        director = [ name['name']['nameText']['text'] for name in director] if director is not None else []
        cast = ", ".join(map(str, cast))
        director = ", ".join(map(str, director))
    else:
        logger.info("API Call for IMDB is failed")
        director = None
        cast = None
    return director,cast

def extract_year(year):
    logger.info("Extract Year from string")
    if '-' in year:
        year = year.split('-')
        return year(0) if len(year) <=1 else year[1]
    else:
        return year
        
def fetch_movie_data(url, genre,html):
    # headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    # }        
    # response = requests.get(url,headers=headers)
    # soup = BeautifulSoup(response.text, 'html.parser')
    logger.info("Extract the Data from html")
    soup = BeautifulSoup(html,'html.parser')
    movies = soup.find_all("li", class_="ipc-metadata-list-summary-item")
        
    for movie in movies:
        title = movie.find('h3',class_='ipc-title__text').text
        year = movie.find('span',class_='sc-300a8231-7 eaXxft dli-title-metadata-item').text
        year = str(extract_year(year))
        year = ''.join(char for char in year if char.isdigit())
        try:
            year = int(year)
        except Exception as e:
            logger.info(f"Year is not a integer value: {year}")
            year = 1800
        rating = movie.find('span',class_="ipc-rating-star--rating").text
        id_value = movie.find('a',class_='ipc-title-link-wrapper')
        id_value = id_value.get('href')
        id_value = id_value.split('/')[2]        
        data = {
        "id": str(id_value),
        "locale": "en-US",
        "location": {
        "latLong": {
            "lat": "12.98",
            "long": "77.58"
        }
        },
        "promotedProvider": None,
        "providerId": None
        }
        director,cast = fetch_director_cast(data)    
        try:
            rating = float(rating)
        except Exception as e:
            logger.info(f"rating is not a float value: {rating}")
            rating = 0.0        
        story = soup.find('div',class_='ipc-html-content-inner-div').text        
        logger.info(f"Data extract for movie {title} and data insertion started")
        Movie.objects.update_or_create(
            title=title,
            genre=genre,
            defaults={
                'year': year,
                'rating': rating,
                'director': director,
                'cast': cast,
                'story': story,  
            },
            )



def lazy_load(driver):
    logger.info(f"Implementing the Lazy loading in website to load more data")
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new content to load
        time.sleep(2)
        
        # Check if the scroll height has changed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Break if no new content is loaded
        last_height = new_height

class MoviePagination(LimitOffsetPagination):
    default_limit = 10  
    max_limit = 100

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['genre']    
    pagination_class = MoviePagination

    def create(self,request):
        logger.info("API hit initialized")
        serializer = GenreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        genre = serializer.validated_data['genre']     
        search_url = f"https://www.imdb.com/search/title/?genres={genre}&view=simple&start=1"
        driver = webdriver.Chrome()
        driver.get(search_url)        
        try:
            lazy_load(driver)
            expand_buttons = driver.find_elements(By.CLASS_NAME, "ipc-see-more__text")
            for button in expand_buttons:
                ActionChains(driver).move_to_element(button).click(button).perform()
                time.sleep(1)
                html = driver.page_source
                fetch_movie_data(search_url,genre,html)
        except Exception as e:
            logger.info(f"Unexpected error: {e}")
            pass        
        finally:
            driver.quit()
        qs = Movie.objects.all()
        serializer = MovieSerializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)