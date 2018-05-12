import json
from pymongo import MongoClient
from flask import Flask, request
from bson import ObjectId


replica1 = 'mongod-0.mongodb-service.default.svc.cluster.local:27017'
replica2 = 'mongod-1.mongodb-service.default.svc.cluster.local:27017'
replica3 = 'mongod-2.mongodb-service.default.svc.cluster.local:27017'
uri = 'mongodb://main_admin:abc123@{},{},{}/?replicaSet=MainRepSet'.format(replica1, replica2, replica3)


client = MongoClient(uri)
db = client.test
agents_db = db.agents

app = Flask(__name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/agents', methods=['GET', 'POST'])
def agents():
    if request.method == 'POST':
        agent = request.get_json(silent=True)
        agent_id = agents_db.insert_one({'codename': 'agent007'}).inserted_id
        return json.dumps({
            'result': True,
            'agent_id': JSONEncoder().encode(agent_id),
        })
    else:
        return json.dumps({
            'result': True,
            'data': [],
        })


@app.route('/agents/<string:codename>', methods=['GET', 'POST'])
def get_agent(codename):
    if request.method == 'POST':
        agent = request.get_json(silent=True)
        print(agent)
        return json.dumps({'result': True})
    else:
        return json.dumps({
            'result': True,
            'agent': {'codename': 'codename'}
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0')
