import json

from flask import Flask, url_for
from flask import request
from flask import render_template
from flask import jsonify

import brain

app = Flask(__name__, static_url_path='/static')

@app.route("/", methods=['GET'])
def page():
    return render_template('index.html')

@app.route('/send', methods=["POST"])
def send():
    request.get_data()
    inmsg = request.form['user_input']
    out = { "message" : str(inmsg) }
    return jsonify(out)

@app.route('/respond', methods=['POST'])
def process():
    request.get_data()
    inmsg = request.form['user_input']
    res = brain.sentence_response(inmsg)
    out = { "outres" : res }
    return jsonify(out)

if __name__ == "__main__":
    app.run()