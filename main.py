# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 21:23:10 2021

@author: hapsar067663
"""

from urllib.request import urlopen
import json
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

my_list = []
url = 'https://ghibliapi.herokuapp.com/films'
response = urlopen(url)
my_list.extend(json.load(response))
df = pd.json_normalize(my_list)

df['release_date'] = pd.to_datetime(df['release_date'])
df['running_time'] = df['running_time'].astype(str).astype(int)
df['rt_score'] = df['rt_score'].astype(str).astype(int)

@app.get("/")
def read_root():
    #return {"Welcome to Studio Ghibli API":""}
    return {"To see average score by each director":"https://hapwul-studio-ghibli.herokuapp.com/average_score_director"}
    return {"To see average score by each producer":"https://hapwul-studio-ghibli.herokuapp.com/average_score_producer"}   
    return {"To show how many films released by each director":"https://hapwul-studio-ghibli.herokuapp.com/productive_director"}
    return {"To show how many films released by each producer":"https://hapwul-studio-ghibli.herokuapp.com/productive_producer"}
    return {"To show top five films from list":"https://hapwul-studio-ghibli.herokuapp.com/top_five"}
    return {"To show top 10 film sorted by the longest duration":"https://hapwul-studio-ghibli.herokuapp.com/longest_film_duration"}
    return {"To show film ranked by its score from highest to lowest":"https://hapwul-studio-ghibli.herokuapp.com/film_rank_score"}

# 1. this function shows average score for films that directed by each director
@app.get("/average_score_director")
def average_score_director():
    result = df.groupby('director')[['rt_score']].mean()
    return result.to_dict(orient='dict')

# 2. this function shows average score for films that directed by each producer
@app.get("/average_score_producer")
def average_score_producer():
    result = df.groupby('producer')[['rt_score']].mean()
    return result.to_dict(orient='dict')

# 3. this function shows how many films released by each director
@app.get("/productive_director")
def productive_director():
    result = df.groupby('director')[['title']].count()
    result = result.sort_values(by=['title'], ascending=[False])
    return result.to_dict(orient='dict')

# 4. this function shows how many films released by each producer
@app.get("/productive_producer")
def productive_producer():
    result = df.groupby('producer')[['title']].count()
    result = result.sort_values(by=['title'], ascending=[False])
    return result.to_dict(orient='dict')

# 5. this function shows top five films from list
@app.get("/top_five")
def top_five():
    selectcolumn = ['title','release_date','running_time']
    result = df[selectcolumn].head(5)
    return result.to_dict(orient='records')

# 6. this function shows top 10 film sorted by the longest duration
@app.get("/longest_film_duration")
def longest_film_duration():
    selectcolumn = ['title','running_time']
    #selectcolumn.sort_values(by=['running_time'], ascending=False)
    result = df[selectcolumn]
    result = result.sort_values(by=['running_time'], ascending=False)
    result = result.head(10)
    return result.to_dict(orient='records')

# 7. this function shows film ranked by its score from highest to lowest
@app.get("/film_rank_score")
def film_rank_score():
    selectcolumn = ['title','rt_score']
    result = df[selectcolumn]
    result = result.sort_values(by=['rt_score'], ascending=False)
    return result.to_dict(orient='records')




