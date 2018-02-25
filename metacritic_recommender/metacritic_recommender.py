import pandas as pd
import numpy as np
import os
import webbrowser

df_critics = pd.read_json("../output/albums.json")

# TODO: Create unique id's
# need to differentiate based on URL -- we have too much overlap from albums with similar names
ratings_df = pd.pivot_table(df_critics, index="publication name", columns="album id")

html = ratings_df.to_html(na_rep="")

with open("review_matrix.html","w") as f:
    f.write(html)