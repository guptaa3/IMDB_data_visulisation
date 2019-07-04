
# coding: utf-8

# # Data visualisation Project - visualisation 3

# imporing necessary libraries and data set

# In[ ]:


import pandas as pd


# In[2]:


from bokeh.plotting import figure , show
from bokeh.layouts import layout, widgetbox, row
from bokeh.models import ColumnDataSource, Div, HoverTool, Legend, CategoricalColorMapper,  Range1d, FactorRange
from bokeh.models.widgets import Slider, Select
from bokeh.io import curdoc, output_notebook


# In[3]:


from bokeh.transform import factor_cmap
from bokeh.palettes import Colorblind


# In[4]:


#output_notebook()


# In[113]:


dataset_titles_prin = pd.read_csv('I:/DCU/SEM1/Lectures/Data Management & Visualisation - CA682 Suzanne Little/project/imdb_project/cleaned data/titles_principle.csv')


# In[112]:


dataset_names = pd.read_csv('I:/DCU/SEM1/Lectures/Data Management & Visualisation - CA682 Suzanne Little/project/imdb_project/cleaned data/names.csv')
dataset_titles_ratings = pd.read_csv('I:/DCU/SEM1/Lectures/Data Management & Visualisation - CA682 Suzanne Little/project/imdb_project/cleaned data/titles_basic_rating.csv')


# Using data set from year 2010 for our analysis

# In[114]:


dataset_titles_ratings = dataset_titles_ratings.drop(dataset_titles_ratings[(dataset_titles_ratings['startYear'] < 2010)].index)


# converting values of rating to numbers

# In[115]:


dataset_titles_ratings.averageRating = pd.to_numeric(dataset_titles_ratings.averageRating)


# selecting data only for movies for our analysis

# In[116]:


dataset_titles_ratings = dataset_titles_ratings.drop(dataset_titles_ratings[(dataset_titles_ratings['titleType'] != 'movie')].index)


# In[120]:


#dataset_titles_prin.head()
#dataset_names.primaryProfession1.unique()


# merging the data of titles prin with titles rating to select only movies after 2010 in titles prin such that cast is selected for movies after 2010

# In[121]:


merged_df_1 = dataset_titles_prin.merge(dataset_titles_ratings, how = 'inner', left_on=dataset_titles_prin.tconst,right_on=dataset_titles_ratings.tconst)


# In[53]:


#merged_df_1.head()


# In[54]:


#merged_df_1=merged_df_1.fillna(0)


# In[55]:


merged_df_1 = merged_df_1.drop(columns = ['key_0','ordering','job','characters','tconst_y','originalTitle','isAdult','runtimeMinutes','genre2'])


# In[56]:


#merged_df_1.head()


# Merging data set names with the above merged data to get the details of the cast and their known for titles which can be used further to  merge with titles rating and get all 4 ratings and num votes

# In[57]:


merged_df_2 = dataset_names.merge(merged_df_1, how = 'inner', left_on=dataset_names.nconst,right_on=merged_df_1.nconst)


# In[58]:


#merged_df_2.head()


# In[59]:


merged_df_2 = merged_df_2.drop(columns = ['key_0','nconst_x','tconst_x','category'])


# In[60]:


#merged_df_2.head()


# In[61]:


merged_df_3 = merged_df_2.merge(dataset_titles_ratings, how = 'inner', left_on=merged_df_2.knownForTitles1,right_on=dataset_titles_ratings.tconst)


# In[62]:


#merged_df_3.head()


# In[63]:


merged_df_3 = merged_df_3.drop(columns=['key_0','primaryTitle_x','titleType_x','primaryTitle_y','isAdult','originalTitle','runtimeMinutes','genre2','runtimeMinutes','genre1_y','genre1_x','averageRating_x', 'numVotes_x', 'tconst', 'titleType_y','startYear_y'])


# In[64]:


#merged_df_3.head()


# In[65]:


merged_df_3 = merged_df_3.drop(columns = ['startYear_x'])


# In[66]:


#merged_df_3.head()


# In[67]:


merged_df_3 = merged_df_3.drop_duplicates()


# In[68]:


#merged_df_3.head()


# Merging the data set 4 times for all known for titles

# In[69]:


merged_df_3 = merged_df_3.merge(dataset_titles_ratings, how = 'inner', left_on=merged_df_3.knownForTitles2,right_on=dataset_titles_ratings.tconst)


# In[70]:


#merged_df_3.head()


# In[71]:


merged_df_3['average_rating1'] = merged_df_3.averageRating_y
merged_df_3['numVotes1'] = merged_df_3.numVotes_y


# In[72]:


merged_df_3['average_rating2'] = merged_df_3.averageRating
merged_df_3['numVotes2'] = merged_df_3.numVotes


# In[73]:


merged_df_3= merged_df_3.drop(columns=['key_0', 'knownForTitles1','knownForTitles2','averageRating_y','numVotes_y','titleType','primaryTitle','originalTitle','isAdult','startYear','runtimeMinutes','genre1','genre2','averageRating','numVotes'])


# In[74]:


#merged_df_3.head()


# In[75]:


merged_df_3 = merged_df_3.merge(dataset_titles_ratings, how = 'inner', left_on=merged_df_3.knownForTitles3,right_on=dataset_titles_ratings.tconst)


# In[76]:


#merged_df_3.head()


# In[77]:


merged_df_3['average_rating3'] = merged_df_3.averageRating
merged_df_3['numVotes3'] = merged_df_3.numVotes


# In[78]:


merged_df_3= merged_df_3.drop(columns=['key_0', 'knownForTitles3','tconst_x','tconst_y','titleType','primaryTitle','originalTitle','isAdult','startYear','runtimeMinutes','genre1','genre2','averageRating','numVotes'])


# In[79]:


#merged_df_3.head()


# In[80]:


#merged_df_3.head()


# In[81]:


merged_df_3 = merged_df_3.merge(dataset_titles_ratings, how = 'inner', left_on=merged_df_3.knownForTitles4,right_on=dataset_titles_ratings.tconst)


# In[82]:


#merged_df_3.head()


# In[83]:


merged_df_3['average_rating4'] = merged_df_3.averageRating
merged_df_3['numVotes4'] = merged_df_3.numVotes
merged_df_3= merged_df_3.drop(columns=['key_0', 'knownForTitles4','titleType','tconst','primaryTitle','originalTitle','isAdult','startYear','runtimeMinutes','genre1','genre2','averageRating','numVotes'])


# In[84]:


#merged_df_3.head()


# Summing the values of 4 average ratings and number of votes

# In[85]:


merged_df_3['average_rating'] = merged_df_3['average_rating1'] + merged_df_3['average_rating2'] + merged_df_3['average_rating3']+ merged_df_3['average_rating4']
merged_df_3['num_Votes'] = merged_df_3['numVotes1'] + merged_df_3['numVotes2'] + merged_df_3['numVotes3']+ merged_df_3['numVotes4']


# In[86]:


merged_df_3 = merged_df_3.drop(columns=['average_rating1','average_rating2','average_rating3','average_rating4','numVotes1','numVotes2','numVotes3','numVotes4'])


# In[87]:


#merged_df_3.head()


# Taking average of the values and calculating the score = rating * num_votes

# In[88]:


merged_df_3['average_rating'] = merged_df_3['average_rating'] /4
merged_df_3['num_Votes'] = merged_df_3['num_Votes'] /4
merged_df_3['score'] = round(merged_df_3['num_Votes']*merged_df_3['average_rating'])


# In[89]:


#merged_df_3.head()


# sorting the values based on score

# In[90]:


merged_df_3 = merged_df_3.sort_values('score', ascending = False)


# Separating the data frames for actors and actresses

# In[91]:


merged_df_female = merged_df_3.drop(merged_df_3[(merged_df_3['primaryProfession1']!='actress')].index)
merged_df_male = merged_df_3.drop(merged_df_3[(merged_df_3['primaryProfession1']!='actor')].index)


# In[92]:


merged_df_female = merged_df_female.head(15)


# In[93]:


merged_df_male = merged_df_male.head(15)


# In[94]:


merged_df_all = pd.concat([merged_df_female, merged_df_male], ignore_index=True)


# In[95]:


merged_df_all = merged_df_all.sort_values('score', ascending = False)


# In[96]:


merged_df_all = merged_df_all.head(15)


# Setting the source which will be updated everytime the values are changed in drop down.

# In[97]:


source= ColumnDataSource(data=dict(x=[], y=[], prof=[], rating = [], vote =[]))


# Setting the figure parameters

# In[100]:


p = figure(plot_height=600,x_range=FactorRange(), y_range = (2000000,9000000), plot_width=700,toolbar_location=None, y_axis_type="log")


# In[101]:


p.add_tools(HoverTool( tooltips=[
    ("Number of votes", "@vote"),
    ("average rating", "@rating"),
    ("score", "@y"),
    ]
    ))
p.xaxis.axis_label_text_font_size ="10pt"
p.yaxis.axis_label_text_font_size= "10pt"
p.title.text_font_size = '12pt'
p.title.align = "center"
p.title.offset =10
p.yaxis.axis_label = 'Score = rating * votes'
p.xaxis.major_label_orientation = 45


# In[102]:


profession_list = ['actor','actress','Overall']
prof_Select = Select(title="Category", value="Overall", options = profession_list)


# In[103]:


def callback(attr, old, new):
        update(prof_sel=prof_Select.value)


# In[104]:


prof_Select.on_change('value',callback)


# In[105]:


def update(prof_sel):
    if(prof_sel == 'actress'):
        df = merged_df_female
        prof_sel_value = 'Actress'
        p.x_range.factors = merged_df_female['primaryName'].unique().tolist()
    elif(prof_sel == 'actor'):
        df = merged_df_male
        prof_sel_value = 'Actor'
        p.x_range.factors = merged_df_male['primaryName'].unique().tolist()
    else :
        df = merged_df_all
        prof_sel_value = 'Actor/Actresses'
        p.x_range.factors = merged_df_all['primaryName'].unique().tolist()
    p.title.text = "Top 15 "+prof_sel_value+" with Highest IMDB score = rating X votes 2010-18" 
    p.xaxis.axis_label = prof_sel_value
    source.data = dict(
        x=df['primaryName'],
        y=df['score'],
        prof=df['primaryProfession1'],
        rating = df['average_rating'],
        vote = df['num_Votes'])
    return (source.data)


# In[106]:


sizing_mode = 'fixed'
inputs = widgetbox(prof_Select,sizing_mode=sizing_mode)
layout = row(p,inputs)


# In[107]:


set_values = update(prof_Select.value)


# In[2]:


profession = merged_df_all.primaryProfession1.unique();


# In[108]:


p.vbar(source=source, x='x',top='y', bottom = 2000000 , width=0.3, color=factor_cmap('prof',palette=['Darkblue','magenta'],factors=profession), legend = 'prof')


# In[109]:


curdoc().add_root(layout)
curdoc().title = "Highest Rated Actor/Actress"


# In[1]:


#show(layout)

