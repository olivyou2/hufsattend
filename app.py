from flask import Flask, request
import json
from account import account
from attendlib import attendlib
from lesson import lesson
from reservate import reservate, reservate_database
from datetime import datetime
from threading import Thread
import time

app = Flask(__name__)
db = reservate_database()
try_max = 5

def reservate_work():
    while True:
        reservates: list[reservate] = db.get_ongoing_reservates()
        now = datetime.now()

        for resv in reservates:
            acc = account(resv.id, resv.pwd)
            lssn = lesson.from_json(resv.lssn_payload)
            att, attid = attendlib.checkAttendance(lssn)

            resv.tries += 1
            if not att:
                resv.result = now.__str__() + ":" + f"Attendance is not progressing ({resv.tries}/{try_max} tries.)"
                if (resv.tries >= try_max):
                    resv.status = 2
            else:
                result = attendlib.attendance(acc, attid, lssn)
                resv.result = now.__str__() + ":" + json.dumps(result)
                resv.status = 1
            print(resv.result)
        
        print(str(len(reservates)) + "개의 예약이 실행되었습니다.")

        time.sleep(1)

reservate_thread = Thread(target=reservate_work)
reservate_thread.start()

@app.route("/lesson", methods=["GET"])
def get_lessons():
    payload = request.args

    if (not payload.__contains__("id")):
        return "Payload must have id"
    
    if (not payload.__contains__("password")):
        return "Payload must have password"
    
    if (not payload.__contains__("year")):
        return "Payload must have year"
    
    if (not payload.__contains__("semester")):
        return "Payload must have semester"

    id = payload["id"]
    password = payload["password"]
    year = payload["year"]
    semester = payload["semester"]

    lssns = account(id, password).getLssns(year, semester)

    return lssns.list()

@app.route("/attend", methods=["POST"])
def attend():
    payload = request.args

    if (not payload.__contains__("id")):
        return "Payload must have id"
    
    if (not payload.__contains__("password")):
        return "Payload must have password"
    
    if (not payload.__contains__("payload")):
        return "Payload must have payload"
    
    id = payload["id"]
    password = payload["password"]
    lssn_payload = payload["payload"]
    lssn_payload = json.loads(lssn_payload)

    acc = account(id, password)

    lssn = lesson.from_json(lssn_payload)
    do, attid = attendlib.checkAttendance(lssn)
    
    if not do:
        return "Attendance check is not in progress"
    
    return attendlib.attendance(acc, attid, lssn)

@app.route("/reservate", methods=["GET"])
def get_reservates():

    res =  list(map(lambda res: res.dict(), db.get_reservates()))
    print(res)
    return res

@app.route("/reservate", methods=["POST"])
def add_reservate():
    payload = request.args

    if (not payload.__contains__("id")):
        return "Payload must have id"
    
    if (not payload.__contains__("password")):
        return "Payload must have password"
    
    if (not payload.__contains__("payload")):
        return "Payload must have payload"
    
    if (not payload.__contains__("time")):
        return "Payload must have time"
    
    id = payload["id"]
    password = payload["password"]
    time = payload["time"]

    lssn_payload = payload["payload"]
    lssn_payload = json.loads(lssn_payload)
    
    dt = datetime.fromtimestamp(float(time))

    db.add_reservate(id, password, lssn_payload, dt)
    return "True"

app.run(host="0.0.0.0", port=80)