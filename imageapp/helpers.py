import requests
from django.conf import settings



def search_image(search_query, quantity):
   url=url = f"https://api.unsplash.com/search/photos?client_id={settings.UNSPLASH_CLIENT_ID}&query={search_query}&page=1&per_page={quantity}"
   response = requests.get(url=url)
   if response.status_code == 200:
       return response.json()
   else:
       # Handle API errors
       return {"results": []} 






#    return response.json()



