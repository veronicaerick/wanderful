from yelpapi import YelpAPI 
import pprint

# set variables for all keys and tokens
consumer_key = "3ntG-6W5C9qnOSQ6QY1ifQ"
consumer_secret = "pYj6X0htclw37_MPafiNkizc2cI"
token = "vmUo0Fon4ay-fmobBYSpezL-vgB9JCYd"
token_secret = "v-i0Kl64JKTvIGM3inuIPgos-QM"

# setting up the search args for the search request
# location is required 
location = "location=barcelona"
# what search term is given
term ="term=tapas"
# how many results we can back
limit = 20

# instantiating a YELP api object with these authentication parameters
yelp_api = YelpAPI(consumer_key, consumer_secret, token, token_secret)

# sending out request, serach_result is the JSON object returned (translates to py dict. per library documentation)
search_results = yelp_api.search_query(location=location, term=term, limit=limit)

# you are creating a pretty printer object
printer = pprint.PrettyPrinter()
# telling the printer to pretty print my results
printer.pprint(search_results)