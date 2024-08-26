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

def get_titles(data):
    titles = []
    
    for item in data:
        titles.append(item['title'])

    return titles

@bp.route('/')
def home():
    genre_data = fetch_all_genres()
    genre_lists = get_genre_lists(genre_data)
    list_genres, list_explicit_genres, list_themes, list_demographics = genre_lists
    return render_template('search.html', 
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
            url = 'https://anime-api-livid.vercel.app/animes?page='
        else:
            url = 'https://anime-api-livid.vercel.app/animes?genres=' + ','.join(map(str, combined_numbers)) + '&page='

        anime_list = fetch_all_anime(url)
        titles = get_titles(anime_list)
        
        # show results
        return render_template('results.html', english_titles=titles)

    except requests.HTTPError as e:
        return render_template('error.html', error_message="Something went wrong: " + str(e))
