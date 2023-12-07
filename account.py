import requests
import fake_useragent
from lesson import lesson, lesson_container

class account:
    id: str
    password: str

    def __init__(self, account_id: str, account_password) -> None:
        self.id = account_id
        self.password = account_password

    def setId(self, id):
        self.id = id

    def setPassword(self, password):
        self.password = password

    def getId(self): return self.id
    
    def getPassword(self): return self.password

    def getLssns(self, year, semester):
        headers = {
            'Accept-Language': 'ko-KR,ko;q=0.9',
            'Origin': 'app://hufs.ac.kr',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection': 'keep-alive',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': fake_useragent.UserAgent().random,
            'Accept': '*/*',
            'Host': 'hufsplusweb2.hufs.ac.kr',
            # 'Content-Length': '218',
            # 'Accept-Encoding': 'gzip, deflate, br',
        }

        data = {
            'from_code': 'hufsPlusAPI',
            'os_type': 'ios',
            'app_version': '2.2.9',
            'id': str(self.getId()),
            'pwd': str(self.getPassword()),
            'year': str(year),
            'semester': str(semester),
        }

        response = requests.post(
            'https://hufsplusweb2.hufs.ac.kr/quick_service/getLectureInfoListForStudentAU_V2',
            headers=headers,
            data=data,
        )
        
        json = response.json()
        values = json["value"]
        lssns: list[lesson] = []

        for value in values:
            org_sect = value[0]
            lssn_cd = value[1]
            faculty_id = value[7]
            subject = value[5]

            lssn = lesson(lssn_cd, faculty_id, year, semester, org_sect, subject)
            lssns.append(lssn)

        lssn_dict = {}
        for lssn in lssns:
            lssn_dict[lssn.lssn_cd] = lssn

        lssns = list(lssn_dict.values())
        
        lssns_container = lesson_container()
        lssns_container.set_lessons(lssns)

        return lssns_container