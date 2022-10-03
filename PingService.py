from flask import Flask, jsonify
from flask_httpauth import HTTPDigestAuth
from requests.auth import HTTPDigestAuth as dauth
import requests
import json

app = Flask(__name__)
auth = HTTPDigestAuth()
app.config['SECRET_KEY'] = 'secret key here'

credentials = {
    'vcu': 'rams'
}

url = 'https://pong-assignment2.herokuapp.com/'

@auth.get_password
def get_pw(username):
    if(username in credentials):
        return credentials.get(username)
    return None

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'page not here'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'message': 'Something is Broken'}), 500

@app.route('/ping', methods=['GET'])
@auth.login_required
def do_ping():
    r = requests.get(url+"pong",auth = dauth("vcu","rams"))
    recording_time = r.elapsed.total_seconds() * 10000
    pingpong_t = recording_time
    return jsonify({"time":pingpong_t})

if __name__ == '__main__':
    app.run()