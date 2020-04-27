import json
import time
from datetime import datetime

import flask
from flask import Flask, render_template
from flask_cors import CORS
import requests
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

total_it_students = 627

goals = [
    {
        "percent": 18.3,
        "event": "Jonathan Sjölander (ITA), will run Göteborgsvarvet in kilt. Video proof will be provided."
    },
    {
        "percent": 20,
        "event": "Simon Hansson (vSO) and Jonathan Sjölander (ITA) will dye their hair in the color of whichever the student division gets the best voting results."
    },
    {
        "percent": 25,
        "event": 'The entire management team will record a music video to the epic song "Chalmers är inte nördigt".'
    },
    {
        "percent": 30,
        "event": "Emilia Sandolf (SO) will climb to the peak of Mount Kebnekaise, Sweden's tallest peak, with Chalmers cap and Chalmers flag."
    }
]


def get_votes():
    last_checked = datetime.now()
    url = "https://fumval.herokuapp.com/data.json"
    r = requests.get(url, allow_redirects=True)
    json_data = json.loads(r.text)

    it_votes = get_it_votes(json_data)
    diff = get_most_votes(json_data, it_votes)

    return last_checked, it_votes, diff


def get_it_votes(json_data):
    return int(json_data["per_section"]["Informationsteknik"])


def get_most_votes(json_data, it_votes):
    sections = json_data["per_section"]
    highest_section = ""
    highest_count = 0
    for sect in sections:
        sect_count = sections[sect]
        if sect_count >= highest_count:
            highest_count = sect_count
            highest_section = sect

    diff = highest_count - it_votes
    if diff < 1:
        return "IT is number 1!!"

    return "That is " + str(diff) + " more than " + highest_section




@app.route("/")
def index():
    last_checked, it_votes, diff = get_votes()
    date = last_checked.strftime("%Y-%m-%d %H:%M:%S")
    it_percent = it_votes / total_it_students * 100
    text = "As of " + date + " there are " + str(it_votes) + " IT votes, that is " + str("{:.1f}".format(it_percent)) + "%"

    passed = []
    remaining = []

    for goal in goals:
        if goal["percent"] <= it_percent:
            passed.append(str(goal["percent"]) + "% -- " + goal["event"])
        else:
            remaining.append(str(goal["percent"]) + "% -- " + goal["event"])

    return flask.render_template('page.html', content=text, title="Fum election IT votes", content_two=diff, passed_goals=passed, remaining_goals=remaining)



def host():
    if __name__ == '__main__':
        app.run(host="0.0.0.0")

host()