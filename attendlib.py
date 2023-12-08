import requests
from account import account
from excepts import FailedGetAttendance
from lesson import lesson
import uuid
from datetime import datetime
import math
import fake_useragent

class attendlib:
    def checkAttendance(lssn: lesson):
        headers = {
            'Connection': 'keep-alive',
            'Host': 'atm1.hufs.ac.kr',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Accept-Language': 'ko-KR,ko;q=0.9',
            'Sec-Fetch-Dest': 'empty',
            'Accept': '*/*',
            'User-Agent': fake_useragent.UserAgent().random, 
            'Origin': 'app://hufs.ac.kr',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        data = {
            'from_code': 'hufsPlusAPI',
            'os_type': 'ios',
            'app_version': '2.2.9',
            'org_sect': lssn.org_sect,
            'lssn_cd': lssn.lssn_cd,
        }

        response = requests.post('https://atm1.hufs.ac.kr/student/getRunningAttendanceCheckInfo', headers=headers, data=data)
        data = response.json()

        if (data["status"] != "success"):
            raise FailedGetAttendance()
        
        lssns = data["value"]

        if (len(lssns) > 0):
            return [True, lssns[0][0]]
        else:
            return [False, None]
        
    def attendance(acc: account, attid: str, lssn: lesson):
        headers = {
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Accept-Language': 'ko-KR,ko;q=0.9',
            'Host': 'atm3.hufs.ac.kr',
            'Origin': 'app://hufs.ac.kr',
            'User-Agent': fake_useragent.UserAgent().random,
        }

        data = {
            'from_code': 'hufsPlusAPI',
            'os_type': 'ios',
            'app_version': '2.2.9',
            'attendance_check_id': attid,
            'faculty_id': lssn.faculty_id,
            'uuid': uuid.uuid4().__str__(),
            'id': acc.getId(),
            'pwd': acc.getPassword(),
            'year': lssn.year,
            'semester': lssn.semester,
            'org_sect': lssn.org_sect,
            'lssn_cd': lssn.lssn_cd,
            'server_time': math.floor(datetime.now().timestamp()*1000),
        }

        response = requests.post(
            'https://atm3.hufs.ac.kr/student/applyAttendanceCheckThroughQRCode',
            headers=headers,
            data=data,
            verify=False,
        )

        return response.json()