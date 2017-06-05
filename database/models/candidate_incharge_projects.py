from modules.database_helper import DatabaseHelper


class CandidateInChargeProjects(object):
    def __init__(self, tender_id, candidate_id, incharge_id, owner, name, kick_off_date, deliver_date, finish_date, scale,
                 contract_price, tech_incharge_name):
        self.db = DatabaseHelper()

        self.tender_id = tender_id
        self.candidate_id = candidate_id
        self.incharge_id = incharge_id
        self.owner = owner
        self.name = name
        self.kick_off_date = kick_off_date
        self.deliver_date = deliver_date
        self.finish_date = finish_date
        self.scale = scale
        self.contract_price = contract_price
        self.tech_incharge_name = tech_incharge_name

    def get_project(self):
        command = "SELECT name FROM candidate_incharge_projects WHERE tender_id=%s AND candidate_id=%s AND incharge_id=%s AND owner=%s AND name=%s"
        params = (self.tender_id, self.candidate_id, self.incharge_id, self.owner, self.name)

        result = self.db.query(command, params)
        if result and len(result['data']) == 1:
            return result['data'][0]['name']

        return None

    def save(self):
        project_name = self.get_project()
        if project_name is not None:
            return

        command = """INSERT INTO candidate_incharge_projects 
        (tender_id, candidate_id, incharge_id, owner, name, kick_off_date, deliver_date, finish_date, scale, 
        contract_price, tech_incharge_name)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (self.tender_id, self.candidate_id, self.incharge_id, self.owner, self.name, self.kick_off_date, self.deliver_date,
                  self.finish_date, self.scale, self.contract_price, self.tech_incharge_name)

        self.db.execute(command, params)
