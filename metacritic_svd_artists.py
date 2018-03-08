import pandas as pd
import numpy as np
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

    import pandas.io.sql as sqlio
    sql = """select round(avg(ratings.album_rating),1) as avg_rating, count(ratings.album_rating) as cnt,
    albums.artist, ratings.critic_name, ratings.critic_id from ratings
    JOIN albums ON albums.id = ratings.album_id
    WHERE albums.artist != 'Various Artists'
    group by albums.artist, ratings.critic_name, ratings.critic_id
    order by cnt desc;"""

    ratings_df = sqlio.read_sql_query(sql, conn)
    ratings_pivot = pd.pivot_table(ratings_df, index='critic_name', columns='artist', values='avg_rating',aggfunc=np.max,fill_value=0);

    X = ratings_pivot.values.T # transpose pivot table, getting SVD of critic preferences
    X.shape


    # ### Decomposing the Matrix
    SVD = TruncatedSVD(n_components=12,random_state=17)
    resultant_matrix = SVD.fit_transform(X)

    corr_mat = np.corrcoef(resultant_matrix)

    artist_names = ratings_pivot.columns
    artist_list = list(artist_names)


    # ### User Input
    #artist = input("Enter artist name: ")
    artist = 'Kendrick Lamar'

    selected_artist = artist_list.index(artist)
    corr_selected_artist = corr_mat[selected_artist]

    #corr_range = (corr_selected_artist < 1.0) & (corr_selected_artist > 0.9);
    #suggested_artists = list(artist_names[corr_range])
    id_corr_pairings = dict(zip(artist_names,corr_selected_artist))

    # create data frame linking ids and album correlations so we can sort by correlation!
    corr_df = pd.DataFrame(list(id_corr_pairings.items()),columns=['id','corr'])
    #recommendations = corr_df.loc[(corr_df['corr'] > 0.9) & (corr_df['corr'] < 1.0)]
    corr_df.sort_values(['corr'],ascending=False).head(10)

    # TODO: maybe suggest album with highest MC rating for each artist?

run_profiler()