import csv

if __name__ == '__main__':
    movies_csv = open("Input/movies.csv", 'w', newline='')
    movies_writer = csv.writer(movies_csv)

    movies_writer.writerow(["MovieID", "Title", "Year", "Genre"])

    ratings_csv = open("Input/ratings.csv", 'w', newline='')
    ratings_writer = csv.writer(ratings_csv)

    ratings_writer.writerow(["MovieID", "SourceSite", "Rating", "NumberOfRatings"])

    imdb_file = open('Scraped Data/imdb_movie_list.csv')

    imdb_reader = csv.reader(imdb_file)

    next(imdb_reader)
    i = 1

    for movie in imdb_reader:
        print(i)
        if movie[3] == "":
            movie[3] = "(no_genres_listed)"

        movies_writer.writerow([i, movie[0].encode("ascii", "ignore").decode(), movie[1], movie[3].replace(' ', '|')])

        ratings_writer.writerow([i, "IMDb", movie[2], movie[4]])

        rottentomatoes_file = open('Scraped Data/rotten_tomatoes_movie_list.csv')
        metacritic_file = open('Scraped Data/metacritic_movie_list.csv')

        rottentomatoes_reader = csv.reader(rottentomatoes_file)
        metacritic_reader = csv.reader(metacritic_file)

        next(rottentomatoes_reader)
        next(metacritic_reader)

        for rottentomatoes in rottentomatoes_reader:
            if rottentomatoes[0] == movie[0]:
                ratings_writer.writerow([i, "RottenTomatoes", rottentomatoes[1], rottentomatoes[2]])

        for metacritic in metacritic_reader:
            if metacritic[0] == movie[0]:
                ratings_writer.writerow([i, "Metacritic", metacritic[1], metacritic[2]])

        i = i + 1
