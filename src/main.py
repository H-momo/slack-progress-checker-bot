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
    event = body.get("event", {})
    if (event == {} or event.get("edited") != None):
        return

    # get posted user name and icon
    if (USER_DATA.get(event.get("user")) == None):
        init()
    user_id = event.get("user")
    user_name = USER_DATA.get(user_id).get("name", "unkown user")
    user_icon = USER_DATA.get(event.get("user")).get("img")

    # get posted channel name
    channel_id = event.get("channel")
    if (CHANNEL_DATA.get(channel_id) == None):
        init()
    channel_name = CHANNEL_DATA.get(channel_id, "unkown channel")

    # get message url
    team_id = body.get("team_id")
    timestamp = event.get("ts").replace('.', '')
    message_url = f"https://{team_id}.slack.com/archives/{channel_id}/p{timestamp}"

    # post message
    if (user_icon == None):
        say (
            channel = POST_CHANNEL_ID,
            username = f"🤖 {user_name}",
            text=f"<{message_url}|#{channel_name}>"
        )
    else:
        say (
            channel = POST_CHANNEL_ID,
            username = f"🤖 {user_name}",
            icon_url = user_icon,
            text=f"<{message_url}|#{channel_name}>"
        )

    print(f"Posted: {message_url}")


@app.event('message')
def handle_message_events(body, logger):
    logger.info(body)


def init():
    print("Getting channel and user data...")

    # get channel data
    url = "https://slack.com/api/conversations.list?limit=999"
    headres = {"Authorization": "Bearer " + SLACK_BOT_TOKEN}
    response = requests.get(url, headers=headres)
    response_json = response.json()
    if (response_json.get("channels") == None):
        print("Couldn't get channel data.")
        exit(1)

    global CHANNEL_DATA
    for channel in response_json["channels"]:
        CHANNEL_DATA[channel["id"]] = channel["name"]

    # get user data
    url = "https://slack.com/api/users.list"
    headres = {"Authorization": "Bearer " + SLACK_BOT_TOKEN}
    response = requests.get(url, headers=headres)
    response_json = response.json()
    if (response_json.get("members") == None):
        print("Couldn't get user data.")
        exit(1)

    global USER_DATA
    for member in response_json["members"]:
        try:
            USER_DATA[member["id"]] = {"name": member["real_name"], "img": member["profile"]["image_72"]}
        except KeyError:
            USER_DATA[member["id"]] = {"name": member["name"], "img": member["profile"]["image_72"]}
            print("Error: KeyError of getting user name")

    print("Got channel and user data")


def main():
    print("⚡️ Started!")
    init()

    print(f"The bot will send message to {POST_CHANNEL_ID}")

    SocketModeHandler(app, SLACK_APP_TOCKEN).start()

if __name__ == "__main__":
    main()