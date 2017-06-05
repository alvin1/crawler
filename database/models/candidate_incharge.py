from modules.database_helper import DatabaseHelper


class CandidateIncharge(object):
    def __init__(self, tender_id, candidate_id, incharge_type, incharge_name, incharge_certificate_name,
                 incharge_certificate_no, professional_titles, professional_grade, incharge_id=None):
        self.db = DatabaseHelper()

        self.tender_id = tender_id
        self.candidate_id = candidate_id
        self.incharge_id = incharge_id
        self.incharge_type = incharge_type
        self.incharge_name = incharge_name
        self.incharge_certificate_name = incharge_certificate_name
        self.incharge_certificate_no = incharge_certificate_no
        self.professional_titles = professional_titles
        self.professional_grade = professional_grade

    def get_incharge_id(self):
        command = "SELECT incharge_id FROM candidate_incharge WHERE tender_id=%s AND candidate_id=%s AND incharge_type=%s AND incharge_name=%s"
        params = (self.tender_id, self.candidate_id, self.incharge_type, self.incharge_name)

        result = self.db.query(command, params)
        if result and len(result['data']) == 1:
            return result['data'][0]['incharge_id']

        return None

    def save(self):
        incharge_id = self.get_incharge_id()
        if incharge_id is not None:
            return incharge_id

        self.incharge_id = self.db.generate_id()
        command = """INSERT INTO candidate_incharge 
        (tender_id, candidate_id, incharge_id, incharge_type, incharge_name, incharge_certificate_name,
         incharge_certificate_no, professional_titles, professional_grade)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (self.tender_id, self.candidate_id, self.incharge_id, self.incharge_type, self.incharge_name,
                  self.incharge_certificate_name, self.incharge_certificate_no, self.professional_titles,
                  self.professional_grade)

        self.db.execute(command, params)

        return self.incharge_id
