from modules.database_helper import DatabaseHelper


class FailedPage(object):
    def __init__(self, tender_id, page_url, failed_type):
        self.db = DatabaseHelper()

        self.tender_id = tender_id
        self.page_url = page_url
        self.failed_type = failed_type

    def get_tender_id(self):
        command = 'SELECT tender_id FROM failed_page WHERE tender_id=%s LIMIT 1'
        params = (self.tender_id,)

        result = self.db.query(command, params)
        if result and len(result['data']) == 1:
            return result['data'][0]['tender_id']

        return None

    def save(self):
        tender_id = self.get_tender_id()
        if tender_id is not None:
            print('tender found, will not save again')
            return tender_id

        command = """INSERT INTO failed_page 
        (tender_id, page_url, failed_type)
        VALUES
        (%s, %s, %s)"""
        params = (
        self.tender_id, self.page_url, self.failed_type)

        self.db.execute(command, params)
        return tender_id
