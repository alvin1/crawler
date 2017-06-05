from modules.database_helper import DatabaseHelper


class ReviewBoardMember(object):
    def __init__(self, tender_id, name, company):
        self.db = DatabaseHelper()

        self.tender_id = tender_id
        self.name = name
        self.company = company

    def get_member(self):
        command = 'SELECT name FROM review_board_member WHERE tender_id=%s AND name=%s'
        params = (self.tender_id, self.name)

        result = self.db.query(command, params)
        if result and len(result['data']) == 1:
            return result['data'][0]['name']

        return None

    def save(self):
        name = self.get_member()
        if name is not None:
            return

        command = """INSERT INTO review_board_member 
        (tender_id, name, company)
        VALUES
        (%s, %s, %s)"""
        params = (self.tender_id, self.name, self.company)

        self.db.execute(command, params)
