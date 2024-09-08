# app/routes.py
from flask import render_template, request, Blueprint
from .api import fetch_all_genres, fetch_all_anime
import requests

bp = Blueprint('main', __name__)

LIST_GENRES  = ["Action", "Adventure", "Avant Garde", "Award Winning", "Boys Love", "Comedy", "Drama", "Fantasy", 
               "Girls Love", "Gourmet", "Horror", "Mystery", "Romance", "Sci-Fi", "Slice of Life", "Sports", 
               "Supernatural", "Suspense"]
LIST_EXPLICIT_GENRES  = ["Ecchi", "Erotica", "Hentai"]
LIST_THEMES = ["Adult Cast", "Anthropomorphic", "CGDCT", "Childcare", "Combat Sports", "Crossdressing", "Delinquents", 
               "Detective", "Educational", "Gag Humor", "Gore", "Harem", "High Stakes Game", "Historical", "Idols (Female)", 
               "Idols (Male)", "Isekai", "Iyashikei", "Love Polygon", "Magical Sex Shift", "Mahou Shoujo", "Martial Arts", 
               "Mecha", "Medical", "Military", "Music", "Mythology", "Organized Crime", "Otaku Culture", "Parody", 
               "Performing Arts", "Pets", "Psychological", "Racing", "Reincarnation", "Reverse Harem", "Romantic Subtext", 
               "Samurai", "School", "Showbiz", "Space", "Strategy Game", "Super Power", "Survival", "Team Sports", 
               "Time Travel", "Vampire", "Video Game", "Visual Arts", "Workplace"]
LIST_DEMOGRAPHICS = ["Josei", "Kids", "Seinen", "Shoujo", "Shounen"]

def get_genre_numbers(data, genre_list):
    genre_dict = {}
    genre_numbers_list = []
    for i in range(18 + 3 + 50 + 5):
        genre_dict[data[i].get('name')] = data[i].get('ord_id')

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
    return render_template('search.html', 
                           genres=LIST_GENRES , 
                           explicit_genres=LIST_EXPLICIT_GENRES , 
                           themes=LIST_THEMES, 
                           demographics=LIST_DEMOGRAPHICS)

@bp.route('/search', methods=['POST'])
def search():
    try:
        genre_data = fetch_all_genres()
        selected_genres = request.form.getlist('genres')
        selected_explicit_genres = request.form.getlist('explicit_genres')
        selected_themes = request.form.getlist('themes')
        selected_demographics = request.form.getlist('demographics')
        combined_selections = selected_genres + selected_explicit_genres + selected_themes + selected_demographics
        combined_numbers = get_genre_numbers(genre_data, combined_selections)
        
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
