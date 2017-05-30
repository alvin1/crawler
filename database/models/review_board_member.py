from modules.database import DatabaseHelper


class CandidateProjects(object):
    def __init__(self, tender_id, name, company):
        self.tender_id = tender_id
        self.name = name
        self.company = company

    def save(self):
        command = """INSERT INTO review_board_member 
        (tender_id, name, company)
        VALUES
        (%s, %s, %s)"""
        params = (self.tender_id, self.name, self.company)

        db = DatabaseHelper()
        db.execute(command, params)
