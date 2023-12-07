from datetime import datetime

class reservate:
    id: str
    pwd: str
    lssn_payload: dict
    result: str
    dt: datetime
    status: int
    tries: int

    def dict(self):
        return {
            "id": self.id,
            "pwd": self.pwd,
            "lssn_payload": self.lssn_payload,
            "result": self.result,
            "time": self.dt,
            "status": self.status,
            "tries": self.tries
        }

class reservate_database:
    reservates: list[reservate]

    def __init__(self) -> None:
        self.reservates = list()

    def add_reservate(self, id: str, pwd: str, lssn_payload: dict, time: datetime):
        res = reservate()
        res.id = id
        res.pwd = pwd
        res.lssn_payload = lssn_payload
        res.dt = time
        res.result = "Yet not started"
        res.status = 0
        res.tries = 0
        
        self.reservates.append(res)

    def get_reservates(self):
        return self.reservates
    
    def get_ongoing_reservates(self) -> list[reservate]:
        resvs = filter(lambda reservate: (reservate.dt < datetime.now()) and (reservate.status == 0), self.reservates)
        resvs = list(resvs)

        return resvs