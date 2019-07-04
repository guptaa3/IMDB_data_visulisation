
# coding: utf-8

# # Data visualisation Project - Visualisation 1

# Now, that we have cleaned data we can  use it for creating visualisations and finding interesting things from it.

# Importing necessary libraries and the data set

# In[4]:


import pandas as pd
import numpy as np


# In[5]:


from bokeh.plotting import figure , show
from bokeh.layouts import layout, widgetbox, row
from bokeh.models import ColumnDataSource, Div, HoverTool, Legend
from bokeh.models.widgets import Slider, Select
from bokeh.io import curdoc, output_notebook


# In[6]:


from bokeh.transform import factor_cmap
from bokeh.palettes import Colorblind


# In[5]:


#output_notebook()


# In[6]:


dataset_names = pd.read_csv('I:/DCU/SEM1/Lectures/Data Management & Visualisation - CA682 Suzanne Little/project/imdb_project/cleaned data/names.csv',index_col= 'nconst')


# In[7]:


dataset_titles_ratings = pd.read_csv('I:/DCU/SEM1/Lectures/Data Management & Visualisation - CA682 Suzanne Little/project/imdb_project/cleaned data/titles_basic_rating.csv',index_col= 'tconst')


# In[8]:


dataset_titles_prin = pd.read_csv('I:/DCU/SEM1/Lectures/Data Management & Visualisation - CA682 Suzanne Little/project/imdb_project/cleaned data/titles_principle.csv',index_col= 'tconst')


# In[295]:


#dataset_titles_prin.head()


# In[296]:


#dataset_titles_ratings.head()


# In[297]:


#dataset_names.head()


# In[298]:


#dataset_titles_ratings.describe(include = 'all')


# We want to concentrate on Comedy, Romance, Drama, Horror and Action genres for our visualisations

# In[1]:


genres = ['Comedy','Romance', 'Drama','Horror','Action']


# In[10]:


#genres


# Creating a source data for our visualisation.

# In[7]:


source = ColumnDataSource(data=dict(x=[], y=[], genre=[], title=[], year=[]))


# Defining the parameters for the visualisation.

# In[8]:


p = figure(plot_height=650, plot_width=700, title="" , toolbar_location=None, x_range=(10,100000),y_range=(0,11),x_axis_type="log")


# In[9]:


c = p.circle(x="x", y="y", source=source, size=7, color=factor_cmap('genre', palette=Colorblind[5], factors=genres), legend='genre')


# In[51]:


p.add_tools(HoverTool( tooltips=[
    ("Title", "@title"),
    ("Genre", "@genre"),
    ]
    ))
p.legend.location = "top_right"
p.legend.orientation = "horizontal"
p.xaxis.axis_label_text_font_size ="16pt"
p.yaxis.axis_label_text_font_size= "16pt"
p.title.text_font_size = '20pt'
p.title.align = "center"
p.title.offset =10


# In[52]:


p.xaxis.axis_label = 'Number of Votes'
p.yaxis.axis_label = 'Average Rating'


# Defining the call back function, to be called on change of slider and drop down value

# In[53]:


def callback(attr, old, new):
        print('inside callback')
        update(num=min_year.value,genre_sel=genre_select.value)


# In[54]:


genres_sel_list = genres.append('All')
min_year = Slider(title="Year", start=1950, end=2018, value=2015, step=1)
min_year.on_change('value',callback)
genre_select=Select(title="Genre", value="All", options=genres)
genre_select.on_change('value',callback)


# In[55]:


def select_movies(num,genre_sel):
    selected = dataset_titles_ratings[
        (dataset_titles_ratings.startYear == num)
         & (dataset_titles_ratings.titleType == 'movie') & 
    (dataset_titles_ratings.genre1 != '\\N')
    &((dataset_titles_ratings.genre1 == 'Comedy') | (dataset_titles_ratings.genre1 == 'Romance') |
      (dataset_titles_ratings.genre1 == 'Action') | (dataset_titles_ratings.genre1 == 'Horror') |
      (dataset_titles_ratings.genre1 == 'Drama'))]
    if (genre_sel != "All"):
        selected = selected[selected.genre1.str.contains(genre_sel)==True]
    return selected


# In[56]:


def update(num,genre_sel):
    df = select_movies(num,genre_sel)
    p.title.text = str(len(df)) + " movies selected  for year " + str(min_year.value) 
    source.data = dict(
        x=df['numVotes'],
        y=df['averageRating'],
        genre=df["genre1"],
        title=df.originalTitle,
        year=df["startYear"])
    return (source.data)
    


# In[57]:


sizing_mode = 'fixed'
inputs = widgetbox(min_year,genre_select, sizing_mode=sizing_mode)
layout = row(p,inputs)


# In[58]:


new_value = update(min_year.value,genre_select.value)


# In[59]:


curdoc().add_root(layout)
curdoc().title = "Movies"


# In[60]:


#show(layout)

