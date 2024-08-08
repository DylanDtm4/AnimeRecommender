# app/routes.py
from flask import render_template, request, Blueprint
from .api import fetch_all_genres, fetch_all_anime
import requests

bp = Blueprint('main', __name__)

def get_genre_lists(data):
    result_lists = []
    start = 0
    ranges = [18, 3, 50, 5]
    for range_size in ranges:
        end = start + range_size
        sublist = [data[i].get('name') for i in range(start, end) if i < len(data)]
        result_lists.append(sublist)
        start = end

    return result_lists

def get_genre_numbers(data, genre_list):
    genre_dict = {}
    genre_numbers_list = []
    for i in range(18 + 3 + 50 + 5):
        genre_dict[data[i].get('name')] = data[i].get('mal_id')

    for genre in genre_list:
        genre_numbers_list.append(genre_dict[genre])
    
    return genre_numbers_list

def get_english_titles(data):
    english_titles = []
    
    for item in data:
        for title in item['titles']:
            if title['type'] == 'English':
                english_titles.append(title['title'])

    return english_titles

@bp.route('/')
def home():
    genre_data = fetch_all_genres()
    genre_lists = get_genre_lists(genre_data)
    list_genres, list_explicit_genres, list_themes, list_demographics = genre_lists
    return render_template('index.html', 
                           genres=list_genres, 
                           explicit_genres=list_explicit_genres, 
                           themes=list_themes, 
                           demographics=list_demographics)

@bp.route('/search', methods=['POST'])
def search():
    try:
        genre_data = fetch_all_genres()
        genre_lists = get_genre_lists(genre_data)
        list_genres, list_explicit_genres, list_themes, list_demographics = genre_lists
        full_list_genres = list_genres + list_explicit_genres + list_themes + list_demographics
        selected_genres = request.form.getlist('genres')
        selected_explicit_genres = request.form.getlist('explicit_genres')
        selected_themes = request.form.getlist('themes')
        selected_demographics = request.form.getlist('demographics')
        combined_selections = selected_genres + selected_explicit_genres + selected_themes + selected_demographics
        combined_numbers = [full_list_genres.index(genre) + 1 for genre in combined_selections]
        
        if not combined_numbers:
            url = 'https://anime-api-livid.vercel.app/animes'
        else:
            url = 'https://anime-api-livid.vercel.app/animes?genres=' + ','.join(map(str, combined_numbers))

        anime_list = fetch_all_anime(url)
        english_titles = get_english_titles(anime_list)

        if not english_titles:
            return render_template('index.html', 
                                   genres=list_genres, 
                                   explicit_genres=list_explicit_genres, 
                                   themes=list_themes, 
                                   demographics=list_demographics, 
                                   error="No animes found that match your selections")
        else:
            return render_template('index.html', 
                                   genres=list_genres, 
                                   explicit_genres=list_explicit_genres, 
                                   themes=list_themes, 
                                   demographics=list_demographics, 
                                   english_titles=english_titles)

    except requests.HTTPError as e:
        return render_template('index.html', 
                               genres=list_genres, 
                               explicit_genres=list_explicit_genres, 
                               themes=list_themes, 
                               demographics=list_demographics, 
                               error=f"An error occurred: {e}")
