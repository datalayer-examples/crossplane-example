import os
import base64
import json
import logging
import re
import traceback
import uuid
import datetime

from flask import Flask, request, g, send_from_directory, jsonify, redirect
from flask_cors import CORS

from .postgresql import version, create_tables, insert_user, select_users


log_levels = {
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'warning': logging.WARNING,
    'error': logging.ERROR,
}

logging.basicConfig(
    level=log_levels['info'],
    format='%(asctime)s %(levelname)s: %(message)s',
#    force=True
    )

logger = logging.getLogger("__name__")


PORT = 8765

ROOT_FOLDER='./..'


app = Flask(__name__, static_folder = ROOT_FOLDER)
app.config.update({
    'TESTING': True,
    'DEBUG': True,
})
CORS(
    app, 
    supports_credentials = True,
#    resources={r"/*": {"origins": "*"}},
#    send_wildcard=True,
    )


""" API Endpoints """


@app.route("/api/crossplane", methods=["GET"])
def hello():
    return jsonify({
        'success': True,
        'message': 'Hello Crossplane',
        'db_version': version
        })


@app.route("/api/crossplane/ping", methods=["POST"])
def ping():
    body = request.json
    return jsonify({
        'success': True,
        'pong': body,
        })


@app.route("/api/crossplane", methods=["POST"])
def add():
    body = request.json
    first_name = body.get('firstName')
    last_name = body.get('lastName')
    id = insert_user(first_name, last_name)
    return jsonify({
        'success': True,
        'message': 'User is inserted',
        'user': {
            'id': id,
            'firstName': first_name,
            'lastName': last_name,
            }
        })


@app.route("/api/crossplane/users", methods=["GET"])
def users():
    users = select_users()
    return jsonify({
        'success': True,
        'message': 'Users list',
        'users': users
        })


""" Catch All Routes. """

@app.route('/api/crossplane/examples', methods=["GET"])
def index():
    return """<html>
  <head>
    <title>Crossplane Examples</title>
    <link rel="shortcut icon" href="data:image/x-icon;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAN1wAADdcBQiibeAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAC7SURBVFiF7ZU9CgIxEIXfTHbPopfYc+pJ9AALtmJnZSOIoJWFoCTzLHazxh/Ebpt5EPIxM8XXTCKTxYyMCYwJFhOYCo4JFiMuu317PZwaqEBUIar4YMmskL73DytGjgu4gAt4PDJdzkkzMBloBhqBgcu69XW+1I+rNSQESNDuaMEhdP/Fj/7oW+ACLuACHk/3F5BAfuMLBjm8/ZnxNvNtHmY4b7Ztut0bqStoVSHfWj9Z6mr8LXABF3CBB3nvkDfEVN6PAAAAAElFTkSuQmCC" type="image/x-icon">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" />
  </head>
  <body>
    <h1>Crossplane Examples</h1>
    <img src="/api/library/res/library.svg" width="200" />
  </body>
</html>
"""


@app.route('/api/crossplane/res/<path:path>', defaults = {'folder': 'res'})
def ressource(folder, path):
    return send_from_directory(ROOT_FOLDER + '/' + folder, path)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path.endswith('.js'):
        return send_from_directory(ROOT_FOLDER + '/dist', path)
    return send_from_directory(ROOT_FOLDER + '/dist', 'index.html')


"""  Catch All Exceptions. """

@app.errorhandler(Exception)
def all_exception_handler(e):
    logger.info('-------------------------')
#    traceback.print_exc()
#    logger.info(traceback.extract_stack(e))
    logger.exception(e)
    logger.info('-------------------------')
#    return 'Server Error', 500
    return jsonify({ 
        'success': False, 
        'message': 'Server Error', 
        'exception': e
    })


""" Main Block. """


if __name__ == "__main__":
    logger.info('Server listening on port {0} - Browse http://localhost:{0}'.format(PORT))
    create_tables()
    app.run(
        host = "0.0.0.0", 
        port = PORT,
        threaded = True,
        processes = 1,
    )
