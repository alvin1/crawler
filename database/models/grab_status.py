from modules.database_helper import DatabaseHelper


class GrabStatus(object):
    def __init__(self, page_num=None):
        self.db = DatabaseHelper()

        self.page_num = page_num

    def check_has_page_num(self):
        command = 'SELECT page_num FROM grab_status LIMIT 1'

        result = self.db.query(command)
        if result and len(result['data']) == 1:
            return True

        return False

    def get(self):
        command = 'SELECT page_num FROM grab_status LIMIT 1'

        result = self.db.query(command)
        if result and len(result['data']) == 1:
            return result['data'][0]['page_num']
        return None

    def save(self):
        has_page_num = self.check_has_page_num()
        command = """INSERT INTO grab_status 
                (page_num)
                VALUES
                (%s)"""
        if has_page_num:
            command = """UPDATE grab_status
            SET page_num=%s"""

        params = (self.page_num,)

        self.db.execute(command, params)
