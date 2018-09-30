import requests

API_KEY = '8XTSMCVVBO5CJLT9'

def save_data():

    r = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSFT&apikey=' + API_KEY)
    
    print(r.text)

save_data()

