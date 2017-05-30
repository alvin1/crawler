from modules.database import DatabaseHelper


class CandidateProjects(object):
    def __init__(self, tender_id, candidate_id, owner, name, kick_off_date, deliver_date, finish_date, scale,
                 contract_price, project_incharge_name):
        self.tender_id = tender_id
        self.candidate_id = candidate_id
        self.owner = owner
        self.name = name
        self.kick_off_date = kick_off_date
        self.deliver_date = deliver_date
        self.finish_date = finish_date
        self.scale = scale
        self.contract_price = contract_price
        self.project_incharge_name = project_incharge_name

    def save(self):
        command = """INSERT INTO candidate_projects 
        (tender_id, candidate_id, owner, name, kick_off_date, deliver_date, finish_date, scale,contract_price, 
        project_incharge_name)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (self.tender_id, self.candidate_id, self.owner, self.name, self.kick_off_date, self.deliver_date,
                  self.finish_date, self.scale, self.contract_price, self.project_incharge_name)

        db = DatabaseHelper()
        db.execute(command, params)
