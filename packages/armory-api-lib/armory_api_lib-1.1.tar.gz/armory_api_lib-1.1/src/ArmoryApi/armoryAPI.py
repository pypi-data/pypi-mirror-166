import requests as rq

url = 'https://armorydesbuissons.fr/api/'

# Rank not for first function
# Champions of the season
# Top of the day

def armoryAPI(requestPage):
    if requestPage == 'rank':
        print(requestPage+' Can\'t be used with this function, use armoryAPIUser')
        return
    elif requestPage == 'top':
        r = rq.get(url+requestPage+'?period=day')
        response = r.json()
    elif requestPage == 'champions':
        r = rq.get(url+requestPage)
        response = r.json()
    print(response)
