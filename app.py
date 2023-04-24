import pandas as pd
import streamlit as st
import plotly.express as px

#streamlit run mapp/app.py

#page configuration
st.set_page_config(
    page_title='Movies App',
    page_icon='🎥🎞️',
    layout='wide' 
)

st.title("Movie Suggesting Site" )
st.sidebar.title('🎬Movies App🎬')
st.image('image.jpg',use_column_width=True)

#load data 
@st.cache_data
def load_movies():
    data=pd.read_csv('Moviedataset.csv')
    return data

with  st.spinner('Loading Movies Data...'):
    movies=load_movies()
    st.sidebar.success('Loaded Movies Data')

show_data=st.sidebar.checkbox('Show the Dataset')
if show_data:
    st.subheader('Movies Data')
    st.dataframe(movies, use_container_width=True)

type1=st.sidebar.selectbox('Select Movies Genre',movies['Genre'].unique())
subset= movies[movies['Genre']==type1]
tabs=st.tabs(['Data','Univariate Analysis','Bivariate Analysis'])

#Data Tab
tabs[0].subheader(f'{type1} Movies')
tabs[0].dataframe(subset,use_container_width=True)

#Univariate Analysis Tab
#IMDB Rating
ss=subset.sort_values(by='Rating')
fig1=px.histogram(ss,x='Rating',y='Name',nbins=20)
fig2=px.scatter(ss,x='Name',y='Rating',color='Year')
tabs[1].subheader(f'{type1} stats')
tabs[1].subheader('IMDB_Rating')
tabs[1].plotly_chart(fig1, use_container_width=True)
tabs[1].plotly_chart(fig2, use_container_width=True)

#Votes
ss=subset.sort_values(by='Votes')
fig1=px.histogram(ss,x='Votes',y='Name',nbins=20)
fig2=px.scatter(ss,x='Name',y='Votes',color='Year')
tabs[1].subheader(f'{type1} stats')
tabs[1].subheader('Votes')
tabs[1].plotly_chart(fig1, use_container_width=True)
tabs[1].plotly_chart(fig2, use_container_width=True)


#Bivariate Analysis
x=tabs[2].selectbox('Select X', movies.select_dtypes('number').columns)
y=tabs[2].selectbox('Select Y', movies.select_dtypes('number').columns)
c=tabs[2].selectbox('Select Color',movies.select_dtypes(exclude='number').columns)
fig=px.scatter(subset , x=x, y=y, color=c, hover_data=['Name'],size_max=60)
tabs[2].subheader(f'{type1}: {x} vs {y} by {c}')
tabs[2].plotly_chart(fig, use_container_width=True)
