from pathlib import Path
import json, sys, config

def lockScript():
    lockJson = {'status': True}
    with open('lock.json', 'w') as output:
        json.dump(lockJson, output)

def checkLock():
    return json.loads(Path('lock.json').read_text())['status']

def configCheck(configField, configName):
    assert len(configField) > 0, configName +' not provided. Exiting'

def validate():
    assert checkLock() == False, 'Not unlocked. Or something is wrong with lock.json. Exiting.'
    try:
        checks = [(config.event_auth, 'EventBrite Auth Token'), (config.twilio_sid, 'Twilio SID'), (config.twilio_auth_token, 'Twilio Auth Token'), (config.twilio_msg_svc, 'Twilio Message Service'), (config.twilio_phone, 'Phone number')]
        for check in checks:
            cField, cName = check
            configCheck(cField, cName)
    except AttributeError:
        print('Config.py is missing attributes. Check config.py. Exiting.')
    except NameError:
        print('Check config.py. Something is undefined. Exiting.')

def sendTxt(msg):
    from twilio.rest import Client
    client = Client(config.twilio_sid, config.twilio_auth_token)
    message = client.messages.create(
        messaging_service_sid = config.twilio_msg_svc,
        body = msg,
        to = config.twilio_phone
    )
    lockScript()
    return(message.sid)