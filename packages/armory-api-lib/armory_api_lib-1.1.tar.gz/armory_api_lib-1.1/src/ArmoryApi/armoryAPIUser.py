import requests as rq

url = 'https://armorydesbuissons.fr/api/'

def armoryAPIUser(requestPage, user):
    if requestPage == 'champions':
        print(requestPage+' Can\'t be used with this function, use armoryAPI')
        return
    elif requestPage == 'top':
        print(requestPage+' Can\'t be used with this function, use armoryAPI')
        return
    else:
        r = rq.get(url+requestPage+'?name='+user)
        response = r.json()
        if response['result'] == []:
            print('Error 404, User Not Found')
            return
    print(response)
