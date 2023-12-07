import json

class lesson:
    def __init__(self, lssn_cd, faculty_id, year, semester, org_sect, subject) -> None:
        self.lssn_cd = lssn_cd
        self.faculty_id = faculty_id
        self.year = year
        self.semester = semester
        self.org_sect = org_sect
        self.subject = subject


    lssn_cd: str
    faculty_id: str
    year: str
    semester: str
    org_sect: str
    subject: str

    def from_json( data: dict):
        self = lesson(0, 0, 0, 0, 0, 0)

        self.lssn_cd = data["lssn_cd"]
        self.faculty_id = data["faculty_id"]
        self.year = data["year"]
        self.semester = data["semester"]
        self.org_sect = data["org_sect"]
        self.subject = data["subject"]

        return self 

class lesson_container:
    lssns: list[lesson]

    def set_lessons(self, lssns: list[lesson]):
        self.lssns = lssns

    def get_by_subject(self, subject: str):
        filtered = filter(lambda lssn: lssn.subject == subject, self.lssns)
        filtered = list(filtered)

        if (len(filtered) > 0): return filtered[0]
        else: return None

    def get_by_lssn_cd(self, lssn_cd: str):
        filtered = filter(lambda lssn: lssn.lssn_cd == lssn_cd, self.lssns)
        filtered = list(filtered)

        if (len(filtered) > 0): return filtered[0]
        else: return None

    def list(self):
        data = []

        for lssn in self.lssns:
            data.append({
                "lssn_cd": lssn.lssn_cd,
                "faculty_id": lssn.faculty_id,
                "org_sect": lssn.org_sect,
                "year": lssn.year,
                "semester": lssn.semester,
                "subject": lssn.subject
            })

        return data 
    
    def json(self):
        arr = self.list()

        return json.dumps(arr)