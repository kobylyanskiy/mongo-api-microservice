import json
import pymongo
from flask import Flask, request
from bson import ObjectId


replica1 = 'mongod-0.mongodb-service.default.svc.cluster.local:27017'
replica2 = 'mongod-1.mongodb-service.default.svc.cluster.local:27017'
replica3 = 'mongod-2.mongodb-service.default.svc.cluster.local:27017'
uri = 'mongodb://main_admin:abc123@{},{},{}/?replicaSet=MainRepSet'.format(replica1, replica2, replica3)


client = pymongo.MongoClient(uri)
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
        agent = request.get_json(force=True)
        try:
            agent_id = agents_db.insert_one(dict(agent)).inserted_id
        except pymongo.errors.DuplicateKeyError:
            return json.dumps({
                'result': False,
                'error_message': 'Agent with this codename already exists',
            })
        except TypeError:
            return json.dumps({
                'result': False,
                'error_message': 'Incorrect input data',
            })

        return json.dumps({
            'result': True,
            'agent_id': JSONEncoder().encode(agent_id),
            'error_message': None,
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
        agent = db.agents.find_one(
            { 'codename': codename }
        )
        return json.dumps({
            'result': True,
            'agent': JSONEncoder.encode(agent)
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0')
