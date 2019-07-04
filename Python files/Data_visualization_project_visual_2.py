
# coding: utf-8

# # Data Visualisation project - visualisation 2

# Importing necessary libraries and the data set

# In[ ]:


import pandas as pd
import numpy as np


# In[1]:


from bokeh.plotting import figure , show
from bokeh.layouts import layout, widgetbox, row
from bokeh.models import ColumnDataSource, Div, HoverTool, Legend, CategoricalColorMapper
from bokeh.models.widgets import Slider, Select
from bokeh.io import curdoc, output_notebook
from bokeh.models.glyphs import MultiLine


# In[2]:


from bokeh.transform import factor_cmap
from bokeh.palettes import Colorblind


# In[31]:


#output_notebook()


# In[4]:


dataset_names = pd.read_csv('I:/DCU/SEM1/Lectures/Data Management & Visualisation - CA682 Suzanne Little/project/imdb_project/cleaned data/names.csv',index_col= 'nconst')
dataset_titles_ratings = pd.read_csv('I:/DCU/SEM1/Lectures/Data Management & Visualisation - CA682 Suzanne Little/project/imdb_project/cleaned data/titles_basic_rating.csv',index_col= 'tconst')
dataset_titles_prin = pd.read_csv('I:/DCU/SEM1/Lectures/Data Management & Visualisation - CA682 Suzanne Little/project/imdb_project/cleaned data/titles_principle.csv',index_col= 'tconst')


# In[45]:


#dataset_titles_ratings.head()


# In[8]:


#dataset_names.head()


# We want to use the data for these 5 genres for our visualisation

# In[5]:


genres = ['Comedy','Romance', 'Drama','Horror','Action']


# In[6]:


#dataset_titles_prin.head()


# In[8]:


dataset_titles_ratings = dataset_titles_ratings.drop(dataset_titles_ratings[(dataset_titles_ratings['genre1'] != 'Action') & (dataset_titles_ratings['genre1'] != 'Comedy')
                                             & (dataset_titles_ratings['genre1'] != 'Horror') & (dataset_titles_ratings['genre1'] != 'Romance')
                                             & (dataset_titles_ratings['genre1'] != 'Drama')].index)


# Lets look at data after the year 1950

# In[9]:


dataset_titles_ratings['startYear'] = pd.to_numeric(dataset_titles_ratings['startYear'])
dataset_titles_ratings = dataset_titles_ratings.drop(dataset_titles_ratings[(dataset_titles_ratings['startYear'] < 1950)].index)


# Removing values other than movies, as we want to see the trend of movies across genres

# In[10]:


dataset_titles_ratings = dataset_titles_ratings.drop(dataset_titles_ratings[(dataset_titles_ratings['titleType']!='movie')].index)


# In[13]:


#dataset_titles_ratings.head()


# Grouping the genre based on year and genre

# In[14]:


dataset_grouped = dataset_titles_ratings.groupby(['startYear','genre1'], as_index=False).agg({"primaryTitle": "count"})


# In[15]:


#dataset_grouped.head()


# Separting the data set into specific genres for easy access of data

# In[16]:


dataset_action = dataset_grouped.drop(dataset_grouped[(dataset_grouped['genre1'] != "Action")].index)


# In[17]:


dataset_Comedy = dataset_grouped.drop(dataset_grouped[(dataset_grouped['genre1'] != "Comedy")].index)


# In[18]:


dataset_Drama = dataset_grouped.drop(dataset_grouped[(dataset_grouped['genre1'] != "Drama")].index)
dataset_Romance = dataset_grouped.drop(dataset_grouped[(dataset_grouped['genre1'] != "Romance")].index)


# In[19]:


dataset_Horror = dataset_grouped.drop(dataset_grouped[(dataset_grouped['genre1'] != "Horror")].index)


# In[20]:


#dataset_action.head()


# Creating 4 sources of data, for each genre

# In[22]:


source_action= ColumnDataSource(data=dict(x=dataset_action['startYear'], y=dataset_action['primaryTitle'], genre=dataset_action['genre1']))
source_comedy= ColumnDataSource(data=dict(x=dataset_Comedy['startYear'], y=dataset_Comedy['primaryTitle'], genre=dataset_Comedy['genre1']))
source_drama= ColumnDataSource(data=dict(x=dataset_Drama['startYear'], y=dataset_Drama['primaryTitle'], genre=dataset_Drama['genre1']))
source_romance= ColumnDataSource(data=dict(x=dataset_Romance['startYear'], y=dataset_Romance['primaryTitle'], genre=dataset_Romance['genre1']))
source_horror= ColumnDataSource(data=dict(x=dataset_Horror['startYear'], y=dataset_Horror['primaryTitle'], genre=dataset_Horror['genre1']))


# Setting the parameters for the figure of visualisation.

# In[139]:


#years with highest number of releases genre wise
p = figure(plot_height=700, plot_width=800, title="Genre wise trend of number of movies over the years" ,toolbar_location=None, x_range=(1950,2018),y_range=(0,2500))


# In[140]:


p.line(x='x', y='y',source =source_action, line_color='darkblue', line_width=2, legend = 'genre')
p.line(x='x', y='y',source =source_romance, line_color='deeppink', line_width=2, legend = 'genre')
p.line(x='x', y='y',source =source_horror, line_color='darkgreen', line_width=2, legend = 'genre')
p.line(x='x', y='y',source =source_comedy, line_color='yellow', line_width=2, legend = 'genre')
p.line(x='x', y='y',source =source_drama, line_color='darkred', line_width=2, legend = 'genre')


# In[141]:


#show(p)


# In[142]:


p.add_tools(HoverTool( tooltips=[
    ("Number of Movies", "@y"),
    ("Genre", "@genre"),
    ("Year","@x")
    ]
    ))

p.legend.location = (322,550)
p.legend.orientation = "horizontal"
p.legend.click_policy="hide"


# In[143]:


p.xaxis.axis_label = 'Year'
p.yaxis.axis_label = 'Number of movies'
p.xaxis.axis_label_standoff = 10
p.xaxis.axis_label_text_font_size ="16pt"
p.yaxis.axis_label_text_font_size= "16pt"
p.title.text_font_size = '20pt'
p.title.align = "center"
p.title.offset =10


# In[144]:


sizing_mode = 'fixed'
inputs = widgetbox(sizing_mode=sizing_mode)
layout = row(p,inputs)


# In[145]:


curdoc().add_root(layout)
curdoc().title = "Movie Genres"


# In[147]:


#show(layout)

