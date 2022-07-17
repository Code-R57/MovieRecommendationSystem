# Movie Recommendation System

The motive of the project is to scrape information of movies from **[IMDb](https://www.imdb.com/)**, **[Rotten Tomatoes](https://www.rottentomatoes.com/)** and **[Metacritic](https://www.metacritic.com/)** to collect the data for a Knowledge Graph that is used as the source of data for a Movie Recommendation System.

## Features

- Scrapes data from the websites.
- Processes the data to remove HTML tags and Unicode values.
- Creates necessary CSV (Comma-Separated Values) file to be imported into the knowledge graph.
- Connects [Neo4j](https://neo4j.com/) Aura Database (knowledge graph built) to the Python program.
- Provides a simple GUI platform to get the top 5 recommended movies based on the movie searched.

## Installation and Running the Code

**Note:** Make sure python and pip are properly installed on the system.

1. **Install the Necessary Libraries** (For 1st time users having one or many of these libraries not installed already)
    1. Run the following in the terminal or cmd:
    ```
    pip install beautifulsoup4
    pip install requests
    pip install html5lib
    pip install regex
    pip install pandas
    pip install scikit-learn
    pip install neo4j
    pip install python-dotenv
    ```  

2. **Scrape Data** (If you want to generate or update the scraped values in Scraped Data folder)
    1. Open the `IMDbScraping.py` file and run the code.  
    It will create or update the `imdb_movie_list.csv` in the Input folder with the current values of the top 250 movies on IMDb.
    2. Repeat `step ii` with `RottenTomatoesScraping.py` and `MetacriticScraping.py` files.  
    It will update the respective files based on the list of movies in the `imdb_movie_list.csv` file.
    3. Now, run the `ProcessingData.py` file.  
    This processes the data into `movies.csv` and `ratings.csv` files, which are used as input files for further data processing.
    4. Open the Jupyter Notebook named `MovieRecommendationSystem.ipynb` and run the program as specified in the notebook.  
    This generates the necessary output files to import to the Neo4j instance.  


3. **Create the Knowledge Graph (Neo4j Graph Database)**
    1. Login into your neo4j account (create if it does not exist).
    1. Create an AuraDB instance.
    1. Save the credentials .env file in the project folder and update the folder name in the `MovieRecommendationSystem.ipynb` and `MovieRecommender.py` files.
    1. Click on import to open the import portal of the neo4j platform.
    1. Add the CSV files present in the `Output` folder.
    1. In the options menu, click `Open model` and select `neo4j_importer_model.json` present in the project folder.
    1. Click on `Run Import`. The values will be imported into the database.  


4. **Run the Movie Recommender**
    1. Now, run the code in the `Connecting the code to Neo4j Database and Running a Sample Query` section of the Jupyter Notebook to test the connectivity of the neo4j database and python code.
    2. Run the `MovieRecommender.py`.  
    It will open the GUI window. Select the criteria as given in the program and select the movie. The output will provide the top 5 recommended movies based on the similarity score.

## Libraries

- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)** - A Python library for pulling data out of HTML and XML files.
- **[requests](https://pypi.org/project/requests/)** - A simple Python library that allows us to send HTTP requests exceptionally easily.
- **[html5lib](https://pypi.org/project/html5lib/)** - A pure-python library for parsing HTML.
- **[csv](https://docs.python.org/3/library/csv.html)** - A module in the standard Python library that implements classes to read and write tabular data in CSV (Comma-Separated Values) format.
- **[pandas](https://pypi.org/project/pandas/)** - A Python package that provides fast, flexible, and expressive data structures designed to make working with "relational" or "labelled" data.
- **[numpy](https://pypi.org/project/numpy/)** - A Python library that provides a multidimensional array object, various derived objects, and an assortment of routines for fast operations on arrays, including mathematical, logical, sorting and much more.
- **[sklearn](https://pypi.org/project/scikit-learn/)** - A Python module for machine learning built on top of SciPy.
- **[neo4j](https://neo4j.com/developer/python/)** - A python library that provides drivers which allows to make a connection to the database and develop applications which create, read, update, and delete information from the graph.
- **[dotenv](https://pypi.org/project/python-dotenv/)** - It reads key-value pairs from a .env file and can set them as environment variables.
- **[tkinter](https://docs.python.org/3/library/tkinter.html)** - It offers multiple options for developing GUI (Graphical User Interface).

## Resources

- **[BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)**
- **[GeeksforGeeks - BeautifulSoup](https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/)**
- **[NithyaKrishnamoorthy - Knowledge Graph](https://github.com/NithyaKrishnamoorthy/KnowledgeGraph)** - Repository on which `MovieRecommendationSystem.py` is based on.
- **[Neo4j Python Driver Documentation](https://neo4j.com/docs/python-manual/current/)**
- **[Neo4j Cypher query language Documentation](https://neo4j.com/docs/cypher-manual/current/)**
- **[freeCodeCamp.org - Tkinter Course](https://www.youtube.com/watch?v=YXPyB4XeYLA)**  
and many more Articles, Documentations, Repositories and Videos.
