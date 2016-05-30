from __future__ import unicode_literals
from yelpapi import YelpAPI 
import pprint
import os

# keys and tokens set up in environ
consumer_key=os.environ['YELP_CONSUMER_KEY']
consumer_secret=os.environ['YELP_CONSUMER_SECRET']
token=os.environ['YELP_ACCESS_TOKEN_KEY']
token_secret=os.environ['YELP_ACCESS_TOKEN_SECRET']

yelp_api = YelpAPI(consumer_key, consumer_secret, token, token_secret)

def get_business_results(location, term="attraction"):
    # create a query with users location, term and limit results to n
    search_response = yelp_api.search_query(location=location, term="attraction", limit=15)
    # contain responses from yelp
    responses = []
    # iterate through 'businesses' response from yelp, append each value needed to
    # a key in a dictionary
    for business in search_response['businesses']:
        responses.append({'name': business['name'],
                        'location': business['location']['display_address'],
                        'latitude': business['location']['coordinate']['latitude'],
                        'longitude': business['location']['coordinate']['longitude'],
                        'rating': business['rating'],
                        'review_count': business['review_count'],
                        'url': business['url'],
                        'image' : business['image_url'].replace('/ms.jpg', '/l.jpg'),
                        'id' : business['id'],
                        'phone': business.get('display_phone')})

    pprint.pprint(responses)
    return responses

