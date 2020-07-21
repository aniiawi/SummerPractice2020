import json
import random

from flask import Flask, request
from prog.publisher import PublisherClass, Var
from prog.msqtt import StartMqtt
import prog.prog_constants as CNST
from .database_for_auth import user, tokens
import hashlib


class WebApp:
    def __init__(self):
        self._pub = PublisherClass()
        self._web = Flask(__name__)

        def auth_token():
            head = request.headers.get('Authorization', None)
            if head is None:
                return False
            tk = head.split(" ")
            if len(tk) != 2:
                return False
            if tk[0] != 'Bearer':
                return False
            name = tokens.get(str(tk[1]), False)
            return name


        @self._web.route("/start")
        def start():
            r_c = self._pub.start_work()
            if r_c:
                return "Started"
            return "Cannot be started"

        @self._web.route("/stop")
        def stop():
            r_c = self._pub.stop_work()
            if r_c:
                return "Stopped"
            return "Cannot be stopped"

        @self._web.route("/list")
        def lst():
            k = {}
            r = self._pub.get_var_list()
            k["len"] = len(r)
            k["vars"] = r
            return json.dumps(k)

        @self._web.route("/add")
        def add():
            nm = request.args.get("name", None)
            b_v = request.args.get("bv", None)
            f_r = request.args.get("f_r", 1.0)
            if nm is None or b_v is None:
                return "ERROR VALS"
            try:
                e = float(b_v)
            except Exception:
                return "BEGIN VAL IS NOT NUMBER"
            self._pub.add_field(Var(nm, b_v, f_r))
            return "OK"

        @self._web.route("/del")
        def delv():
            nm = request.args.get("name", None)
            if nm is None:
                return "ERROR name"
            e = self._pub.del_field(nm)
            if e:
                return "OK"
            return "No VAR with this name"

        @self._web.route('/mqtt')
        def mqtt():
            if not auth_token():
                return "AUTH REQUIRED"
            nm = request.args.get("name", None)
            tp = request.args.get("topic", None)
            if nm is None or tp is None:
                return "ERROR name"
            StartMqtt(CNST.INFLUXDB_ADDR, CNST.MQTT_ADDR, nm, tp)
            return "Variable Added for MQTT"

        @self._web.route('/auth', methods=['POST'])
        def auth():
            nm = request.form.get('username', None)
            ps = request.form.get('password', None)
            if nm is None or ps is None:
                return "ERROR params"
            nm = str(nm)
            if nm not in user:
                return "ERROR user"
            if str(ps) != user[nm]:
                return "ERROR user"
            token = hashlib.sha224(hashlib.sha256((nm+str(random.random())).encode()).digest()).hexdigest()
            tokens[token] = nm
            return json.dumps({"token": token})

    def start(self):
        self._web.run(host="0.0.0.0", port=8011, debug=False)
