from tkinter import *
from neo4j import *
import dotenv
import os

# Change the credentials file to the file downloaded from Neo4j
dotenv.load_dotenv("credentials-04d4e7f0.env")

NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")
AURA_INSTANCENAME = os.environ.get("AURA_INSTANCENAME")

neo4j_driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)

session = neo4j_driver.session()


def submit_movie_title(selected_movie):
    movie_selected = selected_movie.get()

    movie_dropdown_menu.configure(state="disabled")

    movie_title_submit_button = Button(frame, text="Movie Selected", state=DISABLED)
    movie_title_submit_button.grid(row=3, column=10, columnspan=3)

    Label(frame, text="Your top 5 Recommendations are: ").grid(row=4, column=0, columnspan=13)

    query = "MATCH (m:Movie{Title: '" + movie_selected + "'})-[r1:`Similar to`]->(s:Movie)-[r2:`Released in`]->(" \
                                                         "y:Year) return s.Title, r1.SimilarityScore, s.RatingMean, " \
                                                         "y.Year ORDER BY r1.SimilarityScore DESC LIMIT 5"

    result = session.run(query)

    similar_movies = [(record["s.Title"], round(float(record["r1.SimilarityScore"]) * 100, 2),
                       round(float(record["s.RatingMean"]), 2), record["y.Year"]) for record in result]

    Label(frame, text="Title").grid(row=5, column=0, columnspan=6)
    Label(frame, text="Rating").grid(row=5, column=6, columnspan=2)
    Label(frame, text="Release Year").grid(row=5, column=8, columnspan=2)
    Label(frame, text="Chances to Like").grid(row=5, column=10, columnspan=3)

    row = 6

    for movie in similar_movies:
        Label(frame, text=movie[0]).grid(row=row, column=0, columnspan=6)
        Label(frame, text=str(movie[2])).grid(row=row, column=6, columnspan=2)
        Label(frame, text=str(movie[3])).grid(row=row, column=8, columnspan=2)
        Label(frame, text=str(movie[1]) + "%").grid(row=row, column=10, columnspan=3)
        row = row + 1

    start_over_button = Button(frame, text="Start Again", command=lambda: filter_choice(frame))
    start_over_button.grid(row=row, columnspan=6)

    finish_button = Button(frame, text="Close Program", command=frame.quit)
    finish_button.grid(row=row, column=6, columnspan=6)


def submit_select_value(selected_value):
    global movie_dropdown_menu

    filter_value_selected = selected_value.get()

    filter_value_dropdown_menu.configure(state="disabled")

    value_select_submit_button = Button(frame, text="Value Selected", state=DISABLED)
    value_select_submit_button.grid(row=1, column=10, columnspan=3)

    Label(frame, text="Select the Movie: ").grid(row=3, column=0, columnspan=6)

    query = ""

    if filter_selection == "Genre":
        query = "MATCH (g: Genre{Genre: '" + filter_value_selected + "'})<-[b:`Belongs to`]-(m: Movie) return " \
                                                                     "m.Title ORDER BY m.Title "
    if filter_selection == "Year":
        query = "MATCH (y: Year{Year: " + filter_value_selected + "})<-[r:`Released in`]-(m: Movie) return m.Title " \
                                                                  "ORDER BY m.Title "

    result = session.run(query)

    movie_list = [record["m.Title"] for record in result]

    selected_movie = StringVar()
    selected_movie.set(movie_list[0])

    movie_dropdown_menu = OptionMenu(frame, selected_movie, *movie_list)
    movie_dropdown_menu.grid(row=3, column=6, columnspan=4)

    movie_title_submit_button = Button(frame, text="Select Movie", command=lambda: submit_movie_title(selected_movie))
    movie_title_submit_button.grid(row=3, column=10, columnspan=3)


def submit_sort_type(filter_type):
    global filter_value_dropdown_menu

    radio_genre = Radiobutton(frame, variable=filter_type, value="Genre", text="Genre", state=DISABLED)
    radio_year = Radiobutton(frame, variable=filter_type, value="Year", text="Year", state=DISABLED)

    sort_type_submit_button = Button(frame, text="Criteria Selected", command=submit_sort_type, state=DISABLED)

    radio_genre.grid(row=0, column=6, columnspan=2)
    radio_year.grid(row=0, column=8, columnspan=2)
    sort_type_submit_button.grid(row=0, column=10, columnspan=3)

    global filter_selection
    filter_selection = filter_type.get()

    options = []

    if filter_selection == "Genre":
        Label(frame, text="Select the Genre of the Movie: ").grid(row=1, column=0, columnspan=6)

        query = "MATCH (g: Genre) WHERE g.Genre <> '(no_genres_listed)' return g.Genre ORDER BY g.Genre"
        result = session.run(query)

        options = [record["g.Genre"] for record in result]

    if filter_selection == "Year":
        Label(frame, text="Select the year of Release: ").grid(row=1, column=0, columnspan=6)

        query = "MATCH (y: Year) return y.Year ORDER BY y.Year"
        result = session.run(query)

        options = [str(record["y.Year"]) for record in result]

    selected_value = StringVar()
    selected_value.set(options[0])

    filter_value_dropdown_menu = OptionMenu(frame, selected_value, *options)
    filter_value_dropdown_menu.grid(row=1, column=6, columnspan=4)

    value_select_submit_button = Button(frame, text="Select Value", command=lambda: submit_select_value(selected_value))
    value_select_submit_button.grid(row=1, column=10, columnspan=3)


def filter_choice(old_frame):
    old_frame.destroy()

    global frame
    frame = Frame(root)
    frame.pack()

    filter_type = StringVar()
    filter_type.set("Genre")

    sort_by_label = Label(frame, text="Search Movie by: ")

    radio_genre = Radiobutton(frame, variable=filter_type, value="Genre", text="Genre")
    radio_year = Radiobutton(frame, variable=filter_type, value="Year", text="Year")

    sort_type_submit_button = Button(frame, text="Select Criteria", command=lambda: submit_sort_type(filter_type))

    sort_by_label.grid(row=0, column=0, columnspan=6)
    radio_genre.grid(row=0, column=6, columnspan=2)
    radio_year.grid(row=0, column=8, columnspan=2)
    sort_type_submit_button.grid(row=0, column=10, columnspan=3)


if __name__ == '__main__':
    root = Tk()
    root.title("Movie Recommender")

    filter_choice(Frame(root))

    root.mainloop()
    neo4j_driver.close()
