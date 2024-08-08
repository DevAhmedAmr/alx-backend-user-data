import requests

# Original search term
search_term = "American landmark"

# URL encode the search term
encoded_search_term = requests.utils.quote(search_term)

print(encoded_search_term)
