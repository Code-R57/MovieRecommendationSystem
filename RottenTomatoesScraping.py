from bs4 import BeautifulSoup
import requests
import csv
import html5lib
import time
import re


def get_rating_data(soup):
    rating = soup.find('score-board', {'data-qa': 'score-panel'})['audiencescore']
    numberOfRatings = soup.find('a', {'slot': 'audience-count'}).text
    numberOfRatings = re.sub('[^0-9]', "", numberOfRatings)

    if rating != "":
        rating = float(rating) / 10
        return (rating, numberOfRatings)

    return False


def search_movie(title):
    while True:
        SEARCH_URL = "https://www.rottentomatoes.com/search?search=" + title

        request = requests.get(SEARCH_URL)
        soup = BeautifulSoup(request.content, "html5lib")

        if "Rotten Tomatoes: Movies | TV Shows | Movie Trailers | Reviews - Maintenance in Progress" not in str(soup):
            break
        else:
            time.sleep(2)

    if "Sorry, no results found for" not in soup.h1.text:
        print(soup.h1.text)

        if 'data-filter="movie"' in str(soup):
            link = soup.find('search-page-media-row', {'data-qa': 'data-row'}).a['href']

            while True:
                request = requests.get(link)
                soup = BeautifulSoup(request.content, 'html5lib')

                print(soup.title)

                if "Rotten Tomatoes: Movies | TV Shows | Movie Trailers | Reviews - Maintenance in Progress" not in str(
                        soup):
                    break
                else:
                    time.sleep(2)

            rating_data = get_rating_data(soup)

            if rating_data != False:
                writer.writerow([title, rating_data[0], rating_data[1]])


if __name__ == '__main__':

    with open("Scraped Data/rotten_tomatoes_movie_list.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Title", "Rating", "NumberOfRatings"])

        file = open('Scraped Data/imdb_movie_list.csv')
        csvreader = csv.reader(file)

        next(csvreader)

        BASE_URL = "https://www.rottentomatoes.com/m/"

        i = 1

        # Extracting the data (Rating and Number of Ratings) for the top 250 movies as per IMDb
        for movie in csvreader:
            print(i)

            while True:
                request = requests.get(BASE_URL + movie[0].lower().replace(" ", "_"))
                soup = BeautifulSoup(request.content, "html5lib")

                print(soup.title)

                if "Rotten Tomatoes: Movies | TV Shows | Movie Trailers | Reviews - Maintenance in Progress" not in str(
                        soup):
                    break
                else:
                    time.sleep(2)

            if soup.title.text != "Rotten Tomatoes: Movies - Rotten Tomatoes":
                rating_data = get_rating_data(soup)

                if rating_data != False:
                    writer.writerow([movie[0], rating_data[0], rating_data[1]])
                else:
                    search_movie(movie[0])

            else:
                search_movie(movie[0])

            i = i + 1
