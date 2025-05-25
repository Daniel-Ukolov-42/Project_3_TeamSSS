#required imports
import os
import requests
from dotenv import load_dotenv


# Loading in ticketmaster api key from key.env
load_dotenv(dotenv_path = 'key.env')
TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')

#base endpoint for ticketmaster api
BASE_URL = 'https://app.ticketmaster.com/discovery/v2/events.json'


#function to fetch events based on location and keyword
def fetch_events(location='New York', keyword='music', max_results=5):
    '''
    Fetch events from Ticketmaster Discovery API.

    Args:
        location (str): City name.
        keyword (str): Search keyword like music, tech, etc.
        max_results (int): Max number of events to return.

    Returns:
        list of event dictionaries.
    '''
    #API request parameters
    params = {
        'apikey': TICKETMASTER_API_KEY,
        'keyword': keyword,
        'city': location,
        'size': max_results,
        'sort': 'date,asc'
    }

    try:
        #making api request
        response = requests.get(BASE_URL, params=params)
        print('DEBUG URL:', response.url)
        response.raise_for_status()
        data = response.json()

        #extracting events
        events = data.get('_embedded', {}).get('events', [])
        results = []

        #formatting each event into a dictionary
        for event in events:
            results.append({
                'title': event.get('name', 'No title'),
                'summary': event.get('info', 'No description available'),
                'start_time': event.get('dates', {}).get('start', {}).get('localDate', 'N/A'),
                'url': event.get('url', 'N/A'),
                'venue': event.get('_embedded', {}).get('venues', [{}])[0].get('name', 'N/A')
            })

        return results

    #catch and return any failed requests
    except requests.exceptions.RequestException as e:
        return [{'error': f'API request failed: {str(e)}'}]

