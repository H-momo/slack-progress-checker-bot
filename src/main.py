import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests

POST_URL = 'https://slack.com/api/chat.postMessage'

load_dotenv()
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOCKEN = os.environ['SLACK_APP_TOKEN']
POST_CHANNEL_ID = os.environ['POST_CHANNEL_ID']

app = App(token=SLACK_BOT_TOKEN)

CHANNEL_DATA = dict()
USER_DATA = dict()

# if mention
@app.event("app_mention")
def handle_app_mention_events(body, say):
    event = body["event"]

    if (event["subtype"] == "bot_message" or event["subtype"] == "message_changed" or event["subtype"] == "message_deleted"):
        return

    # get posted user name and icon
    user_name = USER_DATA[event["user"]]["name"]
    user_icon = USER_DATA[event["user"]]["img"]

    # get posted channel name
    channel_id = event["channel"]
    if (CHANNEL_DATA[channel_id] == None):
        init();
    try:
        channel_name = CHANNEL_DATA[event["channel"]]
    except KeyError:
        channel_name = "unkown channel"

    # get message url
    team_id = body.get("team_id")
    timestamp = event.get("ts").replace('.', '')
    message_url = f"https://{team_id}.slack.com/archives/{channel_id}/p{timestamp}"

    # post message
    say (
        channel = POST_CHANNEL_ID,
        username = f"🤖 {user_name}",
        icon_url = user_icon,
        text=f"<{message_url}|#{channel_name}>"
    )


@app.event('message')
def handle_message_events(body, logger):
    logger.info(body)


def init():
    print("initializing...")

    # get channel data
    url = "https://slack.com/api/conversations.list?limit=999"
    headres = {"Authorization": "Bearer " + SLACK_BOT_TOKEN}
    response = requests.get(url, headers=headres)
    response_json = response.json()
    global CHANNEL_DATA
    for i in response_json["channels"]:
        CHANNEL_DATA[i["id"]] = i["name"]

    # get user data
    url = "https://slack.com/api/users.list"
    headres = {"Authorization": "Bearer " + SLACK_BOT_TOKEN}
    response = requests.get(url, headers=headres)
    response_json = response.json()
    global USER_DATA
    for i in response_json["members"]:
        try:
            USER_DATA[i["id"]] = {"name": i["real_name"], "img": i["profile"]["image_72"]}
        except KeyError:
            USER_DATA[i["id"]] = {"name": i["name"], "img": i["profile"]["image_72"]}
            print("Error: KeyError of getting user name")

    print("initialized!")


def main():
    print("⚡️ Started!")
    init()

    print(f"Send message to {POST_CHANNEL_ID}")

    SocketModeHandler(app, SLACK_APP_TOCKEN).start()

if __name__ == "__main__":
    main()