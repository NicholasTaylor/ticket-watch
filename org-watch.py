import requests, functions, config, json
from classes import Event

def getOrgs():
    from pathlib import Path
    return json.loads(Path('orgs.json').read_text())

def getOrgStatus(org,latestPage,events):
    page = latestPage
    if latestPage and latestPage > 1:
        url = 'https://www.eventbriteapi.com/v3/organizers/' +str(org) +'/events?page=' +str(latestPage)
    else:
        url = 'https://www.eventbriteapi.com/v3/organizers/' +str(org) +'/events/'
    headers = {
        'Authorization': 'Bearer ' +config.event_auth
    }
    r = requests.get(url, headers=headers)
    eventsList = []
    jsonOutput = r.json()
    print('Org: %i' % (org))
    try:
        print('Reading from page ' +str(jsonOutput['pagination']['page_number']) +'.')
    except:
        pass
    outputs = jsonOutput['events']
    try:
        continuation = jsonOutput['pagination']['continuation']
    except:
        pass
    has_more_items = jsonOutput['pagination']['has_more_items']
    while has_more_items and continuation:
        page += 1
        print('More data available. Pulling from next page.')
        url2 = url +'?continuation=' +continuation
        headers2 = {  
            'Authorization': 'Bearer ' +config.event_auth
        }
        r2 = requests.get(url2, headers=headers2)
        json2 = r2.json()
        print('Reading from page ' +str(json2['pagination']['page_number']) +'.')
        outputs += json2['events']    
        try:
            continuation = json2['pagination']['continuation']
        except:
            pass
        has_more_items = json2['pagination']['has_more_items']
    for event in outputs:
        candidate = Event(event['id'],event['name']['text'],event['start']['utc'],event['url'])
        if candidate.isFuture() and candidate.id not in events:
            eventsList.append(candidate)
    return page, eventsList

def orgValidate(orgs):
    for org in orgs:
        try:
            checks = [(str(org['orgId']), 'Organization ID'), (org['name'], 'Organization Name')]
            for check in checks:
                cField, cName = check
                functions.configCheck(cField, cName)
        except AttributeError:
            print('Your orgs file is missing certain required key/value pairs. Check orgs.json. Exiting.')
        # Checking if latestPage exists
        try:
            print(str(org['latestPage']))
        except KeyError:
            print('No latestPage found. Setting default to 1. Backfilling from beginning.')
            org['latestPage'] = 1
        # Checking if events array exists
        try:
            print(str(org['events']))
        except KeyError:
            print('No events array found. Not filtering for this run.')
            org['events'] = []

def main(orgs):
    for org in orgs:
        newPage, newEventsList = (getOrgStatus(org['orgId'],org['latestPage'],org['events']))
        org['latestPage'] = newPage
        if len(newEventsList) > 0:
            if len(newEventsList) > 1:
                plural = 's'
            else:
                plural = ''
            msg = 'Heads up. New event' +plural +' from ' +org['name'] +':\n'
            for event in newEventsList:
                msg += event.name +': ' +event.url +'\n'
                org['events'].append(event.id)
            functions.sendTxt(msg)
    with open('orgs.json', 'w+') as writeFile:
        json.dump(orgs, writeFile)

functions.validate()
orgs = getOrgs()
orgValidate(orgs)
main(orgs)