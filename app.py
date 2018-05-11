import json
from pymongo import MongoClient
from flask import Flask, request

client = MongoClient('mongod-0',
                     username='admin',
                     password='abc123',
                     authMechanism='MONGODB-CR')

app = Flask(__name__)


@app.route('/agents', methods=['GET', 'POST'])
def agents():
    if request.method == 'POST':
        agent = request.get_json(silent=True)
        print(agent)
        return json.dumps({
            'result': True,
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
