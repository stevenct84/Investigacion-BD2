import streamlit as st
import movies_info

st.header('Recomendaciones de películas según el usuario')

userid=st.text_input("Ingrese el id del usuario:")

if st.button('Mostar Recomendaciones'):
    movie_list=movies_info.get_movies_by_useid(int(userid))
    st.table(movie_list)