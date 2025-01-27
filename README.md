Web scrapper the project used to extract the data from IMDB Website and store them in DB.

Please find the packages required to setup the project in requirements.txt.

Go to project main directory where manage.py exists.

execute below command to start the service

python manage.py runserver

Endpoints:-

POST Call:- http://localhost:8000/api/movies/

body:-
{
    "genre":"comedy"
}
Need to pass the genre for type of data need to be inserted

will helps you to load the data from IMDB website using web scrapping.

Get Call:- http://localhost:8000/api/movies/

will provide the list of movies inserted while POST call executed.

GET:- http://localhost:8000/api/movies/?search=comedy

Lists the Comedy genre movies available in the DB

By default top 10 movies will be listed. Bcz of pagination implemented. Please pass the limit and offset as per your requirement. we have restricted the limit of 100 maximum to get data at once.

http://localhost:8000/api/movies/?search=comedy&limit=10&offset=0

Implemented the Logiing to get logs in both console and file.

test cases are available and implemented only for GET calls. we can implemented many other cases while inserting and other activites.

Please find the command to execute the test cases

pytest .\movies\tests.py

please execute the command from Root project directory.

TODO and enhancements.

we should use celery for processing the data after the lazy loading to minimize load.

Asyncio or multi thread programming should be implement after each scroll to insert the data.
Due to time constarints i am not able to implement. I focused on the solutions and then implemtation rather than enhacements at begining