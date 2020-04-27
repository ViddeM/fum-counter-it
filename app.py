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


def get_votes():
    last_checked = datetime.now()
    url = "https://fumval.herokuapp.com/data.json"
    r = requests.get(url, allow_redirects=True)
    json_data = json.loads(r.text)
    it_votes = get_it_votes(json_data)

    return last_checked, it_votes


def get_it_votes(json_data):
    return int(json_data["per_section"]["Informationsteknik"])


@app.route("/")
def index():
    last_checked, it_votes = get_votes()
    date = last_checked.strftime("%Y-%m-%d %H:%M:%S")
    text = "As of " + date + " there are " + str(it_votes) + " IT votes"
    return flask.render_template('page.html', content=text, title="Fum election IT votes")



def host():
    if __name__ == '__main__':
        app.run(host="0.0.0.0")

host()