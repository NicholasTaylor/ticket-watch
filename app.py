from pathlib import Path
import json, sys, requests

def sendTxt():
    from twilio.rest import Client
    msg = 'Good news! Status change: ' +str(currentStatus) +' Gooo!\nhttps://www.eventbrite.com/e/' +str(eventId)
    client = Client(twilio_sid, twilio_auth_token)
    message = client.messages.create(
        messaging_service_sid = twilio_msg_svc,
        body = msg,
        to = twilio_phone
    )
    lockScript()
    return(message.sid)

def checkStatus():
    url = 'https://www.eventbriteapi.com/v3/events/' +str(eventId) +'/ticket_classes/'
    headers = {
        'Authorization': 'Bearer ' +key
    }
    r = requests.get(url, headers=headers)
    status = r.json()['ticket_classes'][0]['on_sale_status']
    return status

def lockScript():
    lockJson = {'status': True}
    with open('lock.json', 'w') as output:
        json.dump(lockJson, output)

def getPayload():
    config = json.loads(Path('config.json').read_text())
    return config['authRaw'], config['eventId'], config['twilio_sid'], config['twilio_auth_token'], config['twilio_msg_svc'], config['twilio_phone']

def checkLock():
    return json.loads(Path('lock.json').read_text())['status']


assert checkLock() == False, 'Not unlocked. Or something is wrong with lock.json. Exiting.'
try:
    key, eventId, twilio_sid, twilio_auth_token, twilio_msg_svc, twilio_phone = getPayload()
except:
    print('Error getting key')
    tb = sys.exc_info()[2]
    raise BaseException(...).with_traceback(tb)
#currentStatus = checkStatus()
currentStatus = 'TESTING!'
if currentStatus != 'SOLD_OUT':
    sendTxt()
else:
    pass