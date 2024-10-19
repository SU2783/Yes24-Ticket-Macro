import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('SLACK_BOT_TOKEN')
CHANNEL = os.getenv('SLACK_BOT_CHANNEL')


def notice_message(title, text):
    attachments = [{
        'color': '#ff0000',
        'author_name': 'Slack Bot Notice',
        'title': title,
        'text': text,
    }]
    attachments = json.dumps(attachments)

    response = requests.post(
        url="https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + TOKEN},
        data={"channel": CHANNEL, "attachments": attachments},
    )

    print('Slack Bot Notice:', response.status_code)
