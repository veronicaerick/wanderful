import pprint
from eventbrite import Eventbrite
import os 
import json
from datetime import datetime 

auth_key=os.environ['EVENTBRITE_KEY']

def get_event_results(q, datestring):

    client = Eventbrite(auth_key)
    
    # date = datetime.strptime(datestring, "%Y-%m-%d")
    # params = {"q": q, "start_date.range_start": datestring}
    start_date = datestring+"T00:00:00"
    end_date = datestring+"T23:59:59"
    params = {"q": q, "start_date.range_start": start_date, 
              "start_date.range_end": end_date}

    search_response = client.event_search(**params)
    events = search_response.get('events', [])
    print events
    rendered_responses = []
    
    # # 
    for event in events:
    #     if event.logo and event.logo.url: 
    #         test = event.logo.url
    #     else:
    #         test = 'abc'
        if event.get('logo'):
            image_url = event['logo']['url']
        else:
            image_url = None
        rendered_responses.append({'name': event['name']['html'],
                                    'start': event['start']['local'],
                                    'status': event['status'],
                                    'url': event['url'], 
                                    'locale': event['locale'],
                                    'id': event['id'],
                                    'image':image_url})


    pprint.pprint(rendered_responses)
    return rendered_responses

