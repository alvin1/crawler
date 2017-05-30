from modules.database import DatabaseHelper


class CandidateIncharge(object):
    def __init__(self, tender_id, candidate_id, incharge_id, incharge_type, incharge_name, incharge_certificate_name,
                 incharge_certificate_no, professional_titles, professional_grade):
        self.tender_id = tender_id
        self.candidate_id = candidate_id
        self.incharge_id = incharge_id
        self.incharge_type = incharge_type
        self.incharge_name = incharge_name
        self.incharge_certificate_name = incharge_certificate_name
        self.incharge_certificate_no = incharge_certificate_no
        self.professional_titles = professional_titles
        self.professional_grade = professional_grade

    def save(self):
        command = """INSERT INTO candidate_incharge 
        (tender_id, candidate_id, incharge_id, incharge_type, incharge_name, incharge_certificate_name,
         incharge_certificate_no, professional_titles, professional_grade)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (self.tender_id, self.candidate_id, self.incharge_id, self.incharge_type, self.incharge_name,
                  self.incharge_certificate_name, self.incharge_certificate_no, self.professional_titles,
                  self.professional_grade)

        db = DatabaseHelper()
        db.execute(command, params)
