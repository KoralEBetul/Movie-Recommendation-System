import streamlit as st
import openai
import pandas as pd
from io import StringIO
from streamlit_chat import message  # This is the Streamlit chat component

# Set your OpenAI API key here
openai.api_key = "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"

# Define available genres
GENRES = ['Action', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller']

# Initialize the session state to keep track of the conversation
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.selected_genres = []
    st.session_state.favorite_movies = []


def get_movie_recommendations(prompt):
    """Requests movie recommendations from the GPT model."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a movie expert assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=250,
    )

    # Extract response content
    gpt_response = response['choices'][0]['message']['content']
    return gpt_response


def create_prompt(selected_genres, favorite_movies):
    """Generates a prompt based on the user's preferences."""
    prompt = (
        f"I want you to recommend movies based on the following information:\n"
        f"Preferred genres: {', '.join(selected_genres)}\n"
        f"Favorite movies: {', '.join(favorite_movies)}\n"
        f"Please provide movie recommendations in a table format with the columns: "
        f"Movie Name, Genre, Brief Summary. Keep the response concise."
    )
    return prompt


# Main chat UI logic
if st.session_state.step == 1:
    # Ask for genres
    message("Hi! Let's get started with movie recommendations. What are your preferred genres?", is_user=False)
    selected_genres = st.multiselect("Choose your preferred genres:", GENRES)
    if selected_genres:
        st.session_state.selected_genres = selected_genres
        st.session_state.step = 2

elif st.session_state.step == 2:
    # Ask for favorite movies
    message(
        f"Great! You chose: {', '.join(st.session_state.selected_genres)}. Now, what are your three favorite movies?",
        is_user=False)
    favorite_movies_input = st.text_input("Enter your three favorite movies (separated by commas):")
    if favorite_movies_input:
        st.session_state.favorite_movies = favorite_movies_input.split(',')
        st.session_state.step = 3

elif st.session_state.step == 3:
    # Create prompt and get recommendations
    prompt = create_prompt(st.session_state.selected_genres, st.session_state.favorite_movies)
    gpt_response = get_movie_recommendations(prompt)
    message("Here are some movie recommendations based on your preferences:", is_user=False)

    # Convert GPT response to a dataframe (assuming GPT returns a table-like response)
    try:
        df = pd.read_csv(StringIO(gpt_response), sep="|", header=None, names=["Movie Name", "Genre", "Brief Summary"])
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error parsing GPT response: {e}")

    st.session_state.step = 4

elif st.session_state.step == 4:
    message("If you want more recommendations or to start over, simply refresh the page!", is_user=False)

