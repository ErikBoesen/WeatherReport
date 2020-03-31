#!/usr/bin/env python3

import os
import requests
import random
import re

GROUP_ID = 57653465

bot_id = os.environ.get("GROUPME_BOT_ID")
if not bot_id:
    with open(os.environ["HOME"] + "/groupme_bot_id.txt", "r") as f:
        bot_id = f.read().strip()

def decapitalize(string):
    return string[0].lower() + string[1:]

def get_weather():
    NH_COORDINATES = {
        "x": 41.3083,
        "y": -72.9279
    }

    r = requests.get("https://api.weather.gov/points/{x},{y}/forecast".format(x=NH_COORDINATES["x"],
                                                                              y=NH_COORDINATES["y"]))
    forecast = r.json()["properties"]["periods"][0]["detailedForecast"]
    forecast = decapitalize(forecast)
    return forecast

def get_fun_fact():
    raw = requests.get("http://mentalfloss.com/api/facts?page=4&limit=1").json()
    facts = [entry["fact"] for entry in raw]
    fact = facts[0]

    for tag in ("em", "i"):
        fact = fact.replace("<" + tag + ">", "").replace("</" + tag + ">", "")
    return fact

def get_today_in_history():
    events = requests.get("http://history.muffinlabs.com/date").json()["data"]["Events"]
    event_raw = random.choice(events)
    event_year = event_raw["year"]
    event_text = event_raw["text"]
    event_text = re.sub(r"\[[0-9]+\]", "", event_text)
    return "in " + event_year + ", " + event_text

def get_joke():
    joke = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"}).text
    return joke

def send(message):
    # Recurse when sending multiple messages.
    if isinstance(message, list):
        for item in message:
            send(item, group_id)
        return
    data = {
        "bot_id": bot_id,
        "text": message,
    }
    response = requests.post("https://api.groupme.com/v3/bots/post", data=data)


MAX_MESSAGE_LENGTH = 500

message = "\n\n".join([
    "Good morning ΒΣ! Please find today's weather report script below, prepared for your convenience.",
    "The weather is currently " + get_weather(),
    "Today's fun fact: " + get_fun_fact(),
    "Today in history, " + get_today_in_history(),
    "Today's joke: " + get_joke(),
])

send(message)
