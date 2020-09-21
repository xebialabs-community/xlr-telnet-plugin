#!flask/bin/python
#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
import traceback
import logging
from werkzeug.exceptions import HTTPException, BadRequest, NotFound, Unauthorized
from time import strftime
from logging.handlers import RotatingFileHandler
from functools import wraps
import os, io, json


app = Flask(__name__)
handler = RotatingFileHandler('/var/log/plugin.log', maxBytes=1000000, backupCount=1)
logger_formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
handler.setFormatter(logger_formatter)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)


def getFile( fileName, status="200" ):
     filePath="/mockserver/responses/%s" % fileName
     if not os.path.isfile(filePath):
          app.logger.debug("Cannot find file %s" % fileName)
          raise NotFound({"code": "response_file_not_found", "description": "Unable to load response file"}, 500)

     f = io.open(filePath, "r", encoding="utf-8")
     resp = make_response( (f.read(), status) )
     resp.headers['Content-Type'] = 'application/json; charset=utf-8'
     return resp

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

def requires_auth(f):
    #Determines if the access token is valid
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        if token != "YWRtaW46YWRtaW4=": # admin:admin in base64
          raise Unauthorized()
        return f(*args, **kwargs)
    return decorated

def get_token_auth_header():
    #Obtains the access token from the Authorization Header
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description": "Authorization header is expected"}, 401)
    parts = auth.split()
    if parts[0] != "Basic":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with Basic"}, 401)
    token = parts[1]
    return token

@app.route('/')
def index():
     logRequest(request)
     return "Hello, World!"

@app.route('/exampleResponse/<exampleVariable>')
@requires_auth
def get_exampleResponse(exampleVariable):
     logRequest(request)
     app.logger.debug("The Example Variable is %s" % exampleVariable)
     return getFile("exampleResponse.json")

@app.route('/exampleFileNotFound')
@requires_auth
def get_exampleFileNotFound(exampleVariable):
     logRequest(request)
     return getFile("exampleResponseNotFound.json")


# Use for detailed request debug
def logRequest(request):
     app.logger.debug("**************** LOGGING REQUEST")
     app.logger.debug("request.url=%s" % request.url)
     app.logger.debug("request.headers=%s" % request.headers )
     if request.json:
          app.logger.debug("request.json=%s" % request.json)
     else:
          app.logger.debug("request.data=%s" % request.data)
     app.logger.debug("request.form=%s" % request.form)
     app.logger.debug("****************")

# Added for debug purposes - logging all requests
@app.route("/json")
def get_json():
    data = {"Name":"Some Name","Books":"[Book1, Book2, Book3]"}
    return jsonify(data_WRONG) # INTENTIONAL ERROR FOR TRACEBACK EVENT

@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
    return e


if __name__ == '__main__':
     app.run()
