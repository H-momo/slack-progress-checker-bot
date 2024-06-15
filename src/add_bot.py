import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

load_dotenv()
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

client = WebClient(token=SLACK_BOT_TOKEN)


def join_channel(channel_id):
    print(f"Joining channel {channel_id}...")
    try:
        response = client.conversations_join(channel=channel_id)
        if response["ok"]:
            print(f"Bot successfully joined the channel {channel_id}")
    except SlackApiError as e:
        print(f"Error joining channel: {e.response['error']}")


if __name__ == "__main__":
    print("⚡️ Started!")

    # get channel data
    url = "https://slack.com/api/conversations.list?limit=999"
    headres = {"Authorization": "Bearer " + SLACK_BOT_TOKEN}
    response = requests.get(url, headers=headres)
    response_json = response.json()
    print(response_json)
    channel_ids = []
    for i in response_json["channels"]:
        channel_ids.append(i["id"])

    for channel_id in channel_ids:
        join_channel(channel_id)

    exit()

