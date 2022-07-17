from bs4 import BeautifulSoup
import requests
import csv
import html5lib
import re

if __name__ == '__main__':
    URL = "https://www.imdb.com/chart/top"

    request = requests.get(URL)
    soup = BeautifulSoup(request.content, "html5lib")

    with open("Scraped Data/imdb_movie_list.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Title", "Year", "Rating", "Genre", "NumberOfRatings"])

        movies = {}
        movie_links = {}

        # Extracting the data (Title, Year, Rating and Number of Ratings) fro the top 250 movies as per IMDb
        for movie in soup.find('tbody').findAll('tr'):
            title = movie.find('td', {'class': 'titleColumn'}).a.text
            year = movie.find('td', {'class': 'titleColumn'}).span.text.replace('(', '').replace(')', '')
            link = movie.find('td', {'class': 'titleColumn'}).a['href']
            ratingDetails = movie.find('td', {'class': 'ratingColumn imdbRating'}).strong
            rating = ratingDetails.text
            numberOfRatings = ratingDetails["title"]
            numberOfRatings = re.sub('[^0-9]', "", numberOfRatings)[2:]

            movie_links[title] = link
            movies[title] = [year, rating, numberOfRatings]

        BASE_URL = "https://www.imdb.com/"

        # Extracting the Genres for each of the movie
        for title, link in movie_links.items():
            request = requests.get(BASE_URL + link)
            soup = BeautifulSoup(request.content, 'html5lib')
            print(soup.title)

            genres = ""
            for genre in soup.findAll('a', {'class': 'sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt'}):
                genres = genre.text + " " + genres

            movies[title].append(genres.strip())

        # Writing the Extracted Data into a CSV file
        for title, data in movies.items():
            writer.writerow([title, data[0], data[1], data[3], data[2]])
