from flask import Flask
from flask import request
from flask import Response
from handling import Handler
import json

app = Flask(__name__)

INDEX_NAME = 'contacts'

handler = Handler(INDEX_NAME, wipe_index = True)

@app.route('/contact', methods=['GET','POST'])
def contact_without_name():
    if request.method == 'POST':
        if handler.create_contact(request.json):
            return Response('{"result": "created"}',
                            status = 201,
                            mimetype = 'application/json')
        else:
            return Response('{"result": "failure"}',
                            status = 400,
                            mimetype = 'application/json')
    else:
        res = handler.list_contacts(request.args)
        if res:
            return Response('{"data":' + json.dumps(res) + '}',
                            status = 200,
                            mimetype = 'application/json')
        else:
            return Response('{"result": "failure"}',
                            status = 400,
                            mimetype = 'application/json')

@app.route('/contact/<name>', methods=['GET', 'PUT', 'DELETE'])
def contact_with_name(name):
    if request.method == 'GET':
        res = handler.list_a_contact(name)
        if res:
            return Response('{"data":' + json.dumps(res) + '}',
                            status = 200,
                            mimetype = 'application/json')
        else:
            return Response('{"result": "failure"}',
                            status = 400,
                            mimetype = 'application/json')
    elif request.method == 'PUT':
        if handler.update_contact(request.json):
            return Response('{"result": "updated"}',
                            status = 200,
                            mimetype = 'application/json')
        else:
            return Response('{"result": "failure"}',
                            status = 400,
                            mimetype = 'application/json')
    else:
        if handler.delete_contact(name):
            return Response('{"result": "deleted"}',
                            status = 200,
                            mimetype = 'application/json')
        else:
            return Response('{"result": "failure"}',
                            status = 400,
                            mimetype = 'application/json')
