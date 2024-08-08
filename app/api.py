import requests
import time
import random

def fetch_paginated_data(base_url):
    all_data = []
    page = 1
    max_pages = 25
    max_retries = 5
    base_backoff = 2  # Base backoff time in seconds

    while page <= max_pages:
        url = f"{base_url}&page={page}"
        retries = 0
        
        while retries < max_retries:
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                all_data.extend(data.get('data', []))

                # Check for next page
                if not data.get('pagination', {}).get('has_next_page'):
                    return all_data

                page += 1
                time.sleep(1)  # Fixed delay between requests to reduce request rate
                break  # Exit the retry loop on success

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    if 'Retry-After' in e.response.headers:
                        wait_time = int(e.response.headers['Retry-After'])
                    else:
                        # Calculate exponential backoff with jitter
                        wait_time = base_backoff * (2 ** retries) + random.uniform(0, 1)
                    
                    print(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                    retries += 1
                else:
                    raise

        if retries == max_retries:
            raise Exception("Max retries exceeded")

    return all_data

def fetch_single_page_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data.get('data', [])
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request exception occurred: {e}")
        return None

def fetch_all_genres():
    return fetch_single_page_data('https://anime-api-livid.vercel.app/genres')

def fetch_all_anime(url):
    return fetch_paginated_data(url)

