import streamlit as st
import movieposters as mp
import movies_info

def get_poster(movie_name):
    link = mp.get_poster(title=movie_name)
    return link

def recommend(movie_name):
    movies=[]
    posters=[]
    for movie in movies_info.get_movies(movie_name):
        movies.append(movie[0])
        posters.append(get_poster(movie[0]))
    return movies, posters

st.header('Recomendaciones de películas')

movie_name=st.text_input("Ingrese el nombre de una pelicula:")

if st.button('Mostar Recomendaciones'):
    recommended_movie_names,recommended_movie_posters = recommend(movie_name)
    try:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        
        col4, col5,col6 = st.columns(3)
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
        with col6:
            st.text(recommended_movie_names[5])
            st.image(recommended_movie_posters[5])
    except:
        st.warning("No se encontró una película con ese nombre")
        
