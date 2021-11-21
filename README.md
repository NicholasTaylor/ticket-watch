# ticket-watch
Just a set of Python scripts to stay up to date on EventBrite events. Designed to be run in Cron jobs.
# Setup
First, build out the Docker environment:
```
make build
```
Then, copy the config and org files from the samples:
```
cp orgs_sample.json orgs.json
cp config_sample.py config.py
```
## conifg.py
Just sets a few high level variables so these scripts can interact with EventBrite and Twilio\'s APIs.
```
authRaw = "a1b2c3"
eventId = 1
twilio_sid = "d4e5f6"
twilio_auth_token = "a7b8c9"
twilio_msg_svc = "d0e1f2"
twilio_contacts = [
    {
        "number":"+11234567890",
        "optins":[1,2,3,4]
    },
    {
        "number":"+19876543210",
        "optins":[2,4]
    }
]
```
**Note:** Everything is required here except for the `eventId` variable. That is only required if you\'re going to use `ticket-watch.py`.

**authRaw** - This is your API key from EventBrite. If you don\'t have an API key, just sign in with your EventBrite login at [their API signup page](https://www.eventbrite.com/signin/?referrer=%2Fplatform%2Fapi-keys%2F "their API signup page") and they should set you up. Once you have an API key, just go to [Eventbrite\'s Platform Page](https://www.eventbrite.com/platform/api-keys "Eventbrite\'s Platform Page") and your token should be an alphanumeric string right at the top.
**eventId** - Can be found just by going to the tickets page of the event you want. The `eventId` will be a bunch of numbers at the end of the URI in your browser\'s address bar.
**twilio_sid, twilio_auth_token, twilio_msg_svc** - `twilio_sid` is your Twilio account ID. The `twilio_auth_token` is the corresponding token for your account. `twilio_msg_svc` just pertains to the ID of whatever messaging service you want to use with this project. All 3 of these can be found when you sign up for a Twilio account. For the purposes of this readme, I\'m assuming you have basic Twilio competency. If you don\'t, their [tutorials](https://www.twilio.com/docs/tutorials "tutorials") and [quickstart](https://www.twilio.com/docs/quickstart?filter-product=SMS "quickstart") docs will be great at getting you up to speed.
### twilio_contacts
This is a list of dictionaries for all the people you\'ll potentially want to contact. Each dictionary in the list should only carry two key/value pairs: **number** and **optins**.\
**number** - This is the phone number of what you want to receive texts on. This should follow [E.164](https://www.twilio.com/docs/glossary/what-e164 "E.164") format. Which is essentially `+` then `country code` then the phone number in question. So, in the US, this might be `+15555555555` for 555-555-5555. In the UK, this would be `+442071838750` for `2071 838750`.\
**optins** - This is a list of all the org ID\'s you'll want this person to receive texts about.
## orgs.json
You only need to do something with `orgs.json` if you\'re going to use `org-watch.py`, so it\'s kinda optional to set this up. It\'s just your standard array of objects. Each object is a different org:
```
[
    {
        "orgId": 1, 
        "name": "Sample Org",
        "latestPage": 44, 
        "events": [
            "1234",
            "5678"
        ]
    }
]
```
**orgId** - *(Required)* The ID number for the organizer\'s EventBrite account. You can find this by going to any event ran by an organizer you\'d like to follow. On the event page, click the organizer\'s name in the top hero area (should be right below the title). Your browser will scroll down to a section of the event that\'s all about the organizer (why they don\'t just take you to the organizer\'s page, I have no clue). On this section, you have to click the organizer\'s name **again**. On the resulting page, look up at the address bar. The URI should end in a bunch of numbers. That\'s the organizer\'s ID.
**name** - *(Required)* Just whatever name you want to give the organizer for your own records. This will be what appears in the text messages you\'ll recieve.
**latestPage** - *(Defaults to 1)* All of EventBrite\'s endpoints paginate. This works as a bookmark so the script can pick up from where it left off. After it finishes running, `org-watch.py` will set the `latestPage` value of all orgs to be the last page the script accessed.
**events** - *(Defaults to empty array)* Just a way to store the event ID\'s of events the script already notified you of.
# Running the Scripts
## ticket-watch.py
Designed to be used in case an event sells out of tickets. Will check the `eventId` specified in `config.py` and see if new tickets have since been released, or if a previously bought ticket has been refunded. If it detects tickets are available, it will text the phone specified in `config.py` with the event\' URI. Can be ran with this command:
```
make run-ticket
```
**Note:** If the event has available tickets and the user is texted, this script will go to `lock.json` and change the `status` key to `true`. This will prevent the script from running again and bombarding your phone with the same text over and over. If you wish to reuse this in the future, you\'ll need to manually go to `lock.json` and change `status` back to `false`.
## org-watch.py
Watches all organizers in `orgs.json` and alerts the user via the phone specified in `config.py` in the event new events have been created. Can be ran with this command:
```
make run-org
```
# Automation
I just automate this with Cron jobs on my Raspberry Pi. I assume basic cron competency with this readme. [Crontab Guru](https://crontab.guru/ "Crontab Guru") is a good reference here.