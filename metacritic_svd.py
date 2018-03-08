import pandas as pd
import numpy as np
import pandas.io.sql as sqlio
import psycopg2
import sklearn
from sklearn.decomposition import TruncatedSVD

@profile
def run_profiler():
    try:
        conn = psycopg2.connect("dbname=metacritic user=postgres")
    except:
        print("cannot connect")

    cur = conn.cursor()

    sql = "select * from ratings;"
    #return sqlio.read_sql_query(sql, conn)

    ratings_df = sqlio.read_sql_query(sql, conn) # get_ratings_table();

    ratings_pivot = pd.pivot_table(ratings_df,
                                   index='critic_id',
                                   columns='album_id',
                                   values='album_rating',
                                   aggfunc=np.max,
                                   fill_value=0);

    X = ratings_pivot.values.T # transpose pivot table, getting SVD of critic preferences

    SVD = TruncatedSVD(n_components=12, random_state=17)
    resultant_matrix = SVD.fit_transform(X)
    corr_mat = np.corrcoef(resultant_matrix)

    sql = "SELECT * FROM albums;"
    albums_df = sqlio.read_sql_query(sql, conn)

    album_ids = ratings_pivot.columns
    albums_list = list(album_ids)

    #artist = input("Enter artist name: ")
    #album = input("Enter album name: ")

    artist = "Arcade Fire"
    album = "Funeral"

    # TODO: maybe turn this into a function where you input artist and album name
    # MAYBE join on dataframe in advance of this to reduce sql calls?
    # could we do fuzzy string search in dataframe more quickly?
    sql = "SELECT DISTINCT id, name, artist FROM albums WHERE LOWER(name)=LOWER('"+ album +"') AND LOWER(artist)=LOWER('"+ artist +"') limit 1";
    album = sqlio.read_sql_query(sql, conn)

    try:
        album_id = album['id'][0]
        print("Found album " + album['name'][0] + " by " + album['artist'][0])
    except IndexError:
        print("No album found in database, please try again");
        """SELECT artist 
            FROM albums
            WHERE levenshtein(artist, 'radihead') <= 3
            LIMIT 3;"""
    # put fuzzy string search here for recommendations
    # sql = "SELECT id, name, artist FROM albums WHERE LOWER(name)=LOWER('"+ album +"') AND LOWER(artist)=LOWER('"+ artist +"') limit 1";

    # TODO: automate this w/ a function above!
    selected_album = albums_list.index(album_id)
    corr_selected_album = corr_mat[selected_album]

    # list of album id's related to the selected album
    corr_range = (corr_selected_album < 1.0) & (corr_selected_album > 0.95);

    suggested_albums = list(album_ids[corr_range])
    id_corr_pairings = dict(zip(album_ids,corr_selected_album))

    # create data frame linking ids and album correlations so we can sort by correlation!
    corr_df = pd.DataFrame(list(id_corr_pairings.items()),columns=['id','corr'])
    corr_df.loc[(corr_df['corr'] > 0.95) & (corr_df['corr'] < 1.0)]

    #sql = 'SELECT * FROM albums WHERE id IN' + suggested_albums
    sql = 'select id, name, artist, mc_rating, genres, link from albums where id in %s' % str(tuple(suggested_albums))
    results = sqlio.read_sql_query(sql, conn);

    # Sorting by Metacritic Rating
    corr_results = results.join(corr_df.set_index('id'), on='id')
    corr_results.sort_values(['mc_rating'],ascending=False)


    # Sorting by Correlation
    corr_results.sort_values(['corr'],ascending=False)

run_profiler()