import pprint
from eventbrite import Eventbrite
import os 
import json
from datetime import datetime 

auth_key=os.environ['EVENTBRITE_KEY']

def get_event_results(q, datestring):

    datestring = datetime.strptime(datestring, "%m/%d/%Y")
    datestring = datetime.strftime(datestring, "%Y-%m-%d")
    client = Eventbrite(auth_key)

    
    start_date = datestring+"T01:00:00"
    end_date = datestring+"T23:55:00"
    popular = True
    sort_by = "best"
    categories ="103,110"
    # expand = "https://www.eventbriteapi.com/v3/events/search/?location.address=Indore&expand=organizer,venue&token=JXPOFPSSCU4OQGRAG5RH"
    params = {"q": q, "start_date.range_start": start_date, 
              "start_date.range_end": end_date, "sort_by": sort_by, "popular": popular, "categories": categories, 'expand': 'venue'}
    search_response = client.event_search(**params)
    events = search_response.get('events', [])
    rendered_responses = []
    
    for event in events:
        if event.get('logo'):
            image_url = event['logo']['url']
        else:
            image_url = None
        rendered_responses.append({'name': event['name']['html'],
                                    'start': datetime.strptime(event['start']['local'], ('%Y-%m-%dT%H:%M:%S')),
                                    'status': event['status'],
                                    'url': event['url'], 
                                    'locale': event['locale'],
                                    'id': event['id'],
                                    'description': event['description']['text'],
                                    'image':image_url,
                                    'venue': event['venue']['address'],
                                    'latitude': event['venue']['latitude'],
                                    'longitude': event['venue']['longitude']})

    pprint.pprint(rendered_responses)
    return rendered_responses

