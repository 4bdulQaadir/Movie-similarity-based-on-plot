import pickle
import streamlit as st
import requests

def get_poster(film_id):
    api_url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(film_id)
    response = requests.get(api_url)
    response_data = response.json()
    poster_url = response_data['poster_path']
    full_image_url = "https://image.tmdb.org/t/p/w500/" + poster_url
    return full_image_url

def suggest(film):
    idx = movie_data[movie_data['title'] == film].index[0]
    similarity_scores = sorted(list(enumerate(similarity_matrix[idx])), reverse=True, key=lambda x: x[1])
    suggested_movie_titles = []
    suggested_movie_posters = []
    for i in similarity_scores[1:6]:
        # get the movie poster
        film_id = movie_data.iloc[i[0]].movie_id
        suggested_movie_posters.append(get_poster(film_id))
        suggested_movie_titles.append(movie_data.iloc[i[0]].title)

    return suggested_movie_titles, suggested_movie_posters


st.header('Film Recommendation System')
movie_data = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity_matrix = pickle.load(open('model/similarity.pkl', 'rb'))

film_list = movie_data['title'].values
selected_film = st.selectbox(
    "Type or select a film from the dropdown",
    film_list
)

if st.button('Show Recommendation'):
    suggested_movie_titles, suggested_movie_posters = suggest(selected_film)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
        st.text(suggested_movie_titles[0])
        st.image(suggested_movie_posters[0])
    with col2:
        st.text(suggested_movie_titles[1])
        st.image(suggested_movie_posters[1])

    with col3:
        st.text(suggested_movie_titles[2])
        st.image(suggested_movie_posters[2])
    with col4:
        st.text(suggested_movie_titles[3])
        st.image(suggested_movie_posters[3])
    with col5:
        st.text(suggested_movie_titles[4])
        st.image(suggested_movie_posters[4])

