#142a9da8b4ce440cb4918391a6dbb9d7
import requests

url = ('https://newsapi.org/v2/everything?'
       'q=Tesla&'
       'from=2018-10-06&'
       'sortBy=popularity&'
       'apiKey=142a9da8b4ce440cb4918391a6dbb9d7')

data = requests.get(url).json()

print(data)
