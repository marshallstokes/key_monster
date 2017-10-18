import os
import requests

def slack_message(msg):
    token=os.environ['SLACK_API_KEY']
    channel='@jon'
    bot_name='key_monster_bot'
    icon_url='https://i.pinimg.com/736x/c3/40/97/c34097b924a3a063eaedfcc47a7e336f--cookie-monster-party-cookie-monster-birthday-invitations.jpg'
    payload=data={'token': token, 'channel': channel, 'text': msg, 'username': bot_name, 'icon_url': icon_url}
    r=requests.post('https://slack.com/api/chat.postMessage', payload)
    #print(r.text)

