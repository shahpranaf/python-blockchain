import docker
import json
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from jira import JIRA

options = {
    'server': 'https://jira.tibco.com/'
}


jira = JIRA(options, basic_auth=("username", "password"))
# jira = {}

# os.environ["DOCKER_HOST"] = "tcp://10.245.1.2:2375"

app = Flask(__name__)
CORS(app)
# client = docker.from_env()
client = docker.from_env()

vboxList = {
    "controller": "tcp://10.245.1.2:2375",
    "tciservices1": "tcp://10.245.1.11:2375",
    "tciapps1": "tcp://10.245.1.21:2375",
}


@app.route('/jira', methods=['GET'])
def get_jira_ui():
    return send_from_directory('client', 'jira.html')


@app.route('/', methods=['GET'])
def get_ui():
    return send_from_directory('client', 'index.html')


@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('client/assets', path)


@app.route('/vbox', methods=['POST'])
def set_vbox():
    global client
    values = request.get_json()

    required = ['vbox']
    if not all(key in values for key in required):
        client = docker.from_env()
        response = {
            "message": "Vbox value not found. Set to local"
        }
        return jsonify(response), 201

    if not all(values['vbox'] for key in vboxList):
        client = docker.from_env()
        response = {
            "message": "Docker set to Local"
        }
        return jsonify(response), 200

    client = docker.DockerClient(base_url=vboxList[values['vbox']])

    response = {
        "message": "Docker set to "+values['vbox']
    }
    return jsonify(response), 200


@app.route('/images', methods=['GET'])
def get_images():
    global client
    response = [{
        "attrs": ob.attrs,
        "id": ob.id,
        "labels": ob.labels,
        "short_id": ob.short_id,
        "tags": ob.tags
    } for ob in client.images.list()]

    return jsonify(response), 200


@app.route('/containers', methods=['GET'])
def get_containers():
    global client
    response = [{
        "id": ob.short_id,
        "name": ob.name,
        "image": ob.image.tags[0],
        "long_id": ob.id,
        "status": ob.status,
        "identifier": ob.image.tags[0].split('/')[len(ob.image.tags[0].split('/'))-1]
        # "logs": str(ob.logs(stream=False, tail=5))
    } for ob in client.containers.list(all=True)]
    print(response)

    return jsonify(response), 200


@app.route('/projects', methods=['GET'])
def get_projects():
    # Get all projects viewable by anonymous users.
    projects = jira.projects()

    response = [{
        "id": ob.id,
        "name": ob.name,
        "key": ob.key
    } for ob in projects]

    return jsonify(response), 200


@app.route('/tickets', methods=['GET'])
def get_tickets():
    name = request.args.get('name')
    results = jira.search_issues('assignee='+name, startAt=0, maxResults=100)
    print(results)
    response = [{
        "key": j.key,
        "summary": j.fields.summary,
        "description": j.fields.description,
        "status": j.fields.status.name,
        "permalink": j.permalink()
    } for j in [jira.issue(ob.key) for ob in results]]

    # response = [for id in ids]
    print(response[0])

    return jsonify(response), 200


if __name__ == '__main__':
    print("Running")
    app.run(host='0.0.0.0', port=5005)
