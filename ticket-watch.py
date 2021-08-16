import requests, functions, config

def checkStatus():
    url = 'https://www.eventbriteapi.com/v3/events/' +str(config.eventId) +'/ticket_classes/'
    headers = {
        'Authorization': 'Bearer ' +config.event_auth
    }
    r = requests.get(url, headers=headers)
    print(r.json())
    status = r.json()['ticket_classes'][0]['on_sale_status']
    return status

functions.validate()
currentStatus = checkStatus()
if currentStatus != 'SOLD_OUT':
    msg = 'Good news! Status change: ' +str(currentStatus) +' Gooo!\nhttps://www.eventbrite.com/e/' +str(config.eventId)
    functions.sendTxt(msg)
    functions.lockScript()
else:
    pass