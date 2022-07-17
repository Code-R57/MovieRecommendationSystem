from bs4 import BeautifulSoup
import requests
import csv
import html5lib
import time
import re


def get_rating_data(soup):
    rating = soup.find('td', {'class': 'summary_right pad_btm1'}).a.span.text

    if rating != "tbd":
        numberOfRatings = soup.find('div', {'class': 'user_score_summary'}).find('td', {
            'class': 'summary_left pad_btm2'}).find('span', {'class': 'based_on'}).text
        numberOfRatings = re.sub('[^0-9]', "", numberOfRatings)
        return (rating, numberOfRatings)

    return False


def search_movie(title):
    while True:
        SEARCH_URL = "https://www.metacritic.com/search/movie/" + title.replace(" ", "%20") + "/results?sort=score"

        request = requests.get(SEARCH_URL, headers=user_agent)
        soup = BeautifulSoup(request.content, "html5lib")

        if "503 Service Unavailable" not in str(soup):
            break
        else:
            time.sleep(2)

    if "<p>Enter your search term in the search bar above.</p>" not in str(soup):
        print(soup.title)

        movie_link = soup.find('h3', {'class': 'product_title basic_stat'}).a['href']

        while True:
            request = requests.get("https://www.metacritic.com/" + movie_link, headers=user_agent)
            soup = BeautifulSoup(request.content, 'html5lib')

            print(soup.title)

            if "503 Service Unavailable" not in str(soup):
                break
            else:
                time.sleep(2)

        rating_data = get_rating_data(soup)

        if rating_data != False:
            writer.writerow([title, rating_data[0], rating_data[1]])


if __name__ == '__main__':

    with open("Scraped Data/metacritic_movie_list.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Title", "Rating", "NumberOfRatings"])

        file = open('Scraped Data/imdb_movie_list.csv')
        csvreader = csv.reader(file)

        next(csvreader)

        user_agent = {'User-agent': 'Mozilla/5.0'}

        BASE_URL = "https://www.metacritic.com/movie/"

        i = 1

        # Extracting the data (Rating and Number of Ratings) for the top 250 movies as per IMDb
        for movie in csvreader:
            print(i)

            while True:
                request = requests.get(BASE_URL + movie[0].lower().replace(" ", "-"), headers=user_agent)
                soup = BeautifulSoup(request.content, "html5lib")

                print(soup.title)

                if "503 Service Unavailable" not in str(soup):
                    break
                else:
                    time.sleep(2)

            if soup.title.text != "404 Page Not Found - Metacritic - Metacritic":
                rating_data = get_rating_data(soup)

                if rating_data != False:
                    writer.writerow([movie[0], rating_data[0], rating_data[1]])
                else:
                    search_movie(movie[0])


            else:
                search_movie(movie[0])

            i = i + 1
