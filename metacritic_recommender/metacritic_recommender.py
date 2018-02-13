import pandas as pd
import numpy as np
import os
import webbrowser

df = pd.read_json("../metacritic_crawler/critics.json")

ratings_df = pd.pivot_table(df, index="publication name", columns="album name")

html = ratings_df.to_html(na_rep="")

with open("review_matrix.html","w") as f:
    f.write(html)

