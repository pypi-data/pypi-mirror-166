import hashlib
import json
import sqlite3

import codefast as cf
import requests
from expiringdict import ExpiringDict
from flask import Flask, jsonify, redirect, render_template, request
from hashids import Hashids

from .apps.rabbitmq import Publisher
from .const import Const

cf.info("server go.")
cache = ExpiringDict(max_len=10000, max_age_seconds=86400 * 7)

app = Flask(__name__)


class Response(object):
    def __init__(self, status: int, data: dict = None):
        self.status = status
        self.data = {} if data is None else data

    def to_json(self):
        return jsonify({'status': self.status, 'data': self.data})


@app.route('/nlp', methods=["POST", "GET"])
def nlp_():
    input_json = request.get_json()
    cf.info("recv:", input_json)
    m = hashlib.sha256()
    m.update(str(input_json).encode('utf-8'))
    task_id = m.hexdigest()
    data = {"task_id": task_id, "data": input_json}
    Const.redis.lpush(Const.nlp_list, json.dumps(data))
    resp = Const.redis.blpop(task_id, timeout=60)
    if resp:
        Const.redis.delete(task_id)
    return jsonify(json.loads(resp[1].decode()))


@app.route('/')
def hello_world():
    return "ARE YOU OKAY?"


@app.route('/callback', methods=["POST", "GET"])
def callback_():
    return jsonify({"code": 200, "msg": "SUCCESS"})


@app.route('/redis', methods=["POST", "GET"])
def redis_():
    json_input = request.get_json()
    cf.info(request.json)
    key = json_input.get("key", "key")
    value = json_input.get("value", None)
    if not value:
        return Response(200, {"value": cache.get(key, '')}).to_json()
    else:
        cache[key] = value
        return Response(200, {"value": value}).to_json()


@app.route('/any', methods=["POST", "GET"])
def any_():
    r = Const.redis
    key = 'any_release'
    if r.exists(key):
        return r.get(key).decode()
    else:
        return "no data"

from pyserverless.apps.rabbitmq import AMQPPublisher

@app.route('/amqp', methods=["POST", "GET"])
def _amqp():
    # amqp api
    try:
        js = request.get_json()
        queue_name = js.get('queue_name', 'test')
        message = js.get('message', 'test')
        p = AMQPPublisher(queue_name)
        p.publish(json.dumps(message).encode('utf-8'))
        return jsonify({"result": "success"})
    except Exception as e:
        return jsonify({"result": "fail", "msg": str(e)})


@app.route('/blackhole', methods=["POST", "GET"])
def blackhole_():
    json_input = request.get_json()
    cf.info(request.json)
    Const.redis.lpush('blackhole_list', json.dumps(json_input))
    return Response(200, {"result": "OK"}).to_json()


@app.route("/jsondemo", methods=["POST", "GET"])
def large_json_():
    url = "https://raw.githubusercontent.com/TheProfs/socket-mem-leak/master/10mb-sample.json"
    resp = requests.get(url)
    return jsonify(resp.json())


@app.route('/file', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    print(uploaded_file)
    print(uploaded_file.filename)
    if uploaded_file.filename != '':
        fn = '{}'.format(uploaded_file.filename)
        fn = "/tmp/uploaded"
        uploaded_file.save(fn)
    return "Done"


@app.route('/qxupdate', methods=["POST", "GET"])
def quan_():
    args = request.args
    user = args.get("user", "slipper")
    token = args.get("token", "")
    resp = Const.redis.get(f"{user}_{token}")
    if resp:
        return resp.decode()
    else:
        return "404"


@app.route('/shorten', methods=['POST'])
def index():
    data = request.get_json(force=True)
    cf.info('input data: ' + str(data))
    if not data:
        return {}
    url = data.get('url', '')
    md5 = hashlib.md5(url.encode()).hexdigest()
    uniq_id = Hashids(salt=md5, min_length=6).encode(42)
    cf.info('uniq_id: ' + uniq_id)
    cache[uniq_id] = url
    cf.info('uniq id inserted')
    return jsonify({
        'code': 200,
        'status': 'SUCCESS',
        'url': request.host_url + 's/' + uniq_id
    })


def default_route(path: str) -> str:
    path_str = str(path)
    cf.info('request path: ' + path_str)
    if not path_str.startswith('s/'):
        return ''
    key = path_str.replace('s/', '')
    out_url = cache.get(key)
    if out_url:
        return out_url
    return 'https://www.baidu.com'


@app.route('/<path:path>')
def _default_route(path):
    result = default_route(path)
    cf.info('result is {}'.format(result))
    return redirect(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
