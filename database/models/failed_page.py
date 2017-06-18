from modules.database_helper import DatabaseHelper


class FailedPage(object):
    def __init__(self, tender_id=None, page_url=None, failed_type=None, page_num=None, page_type=None,
                 publish_date=None, reprocessed=None):
        self.db = DatabaseHelper()

        self.tender_id = tender_id
        self.page_url = page_url
        self.failed_type = failed_type
        self.page_num = page_num
        self.page_type = page_type
        self.publish_date = publish_date
        self.reprocessed = reprocessed

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
            return tender_id

        command = """INSERT INTO failed_page 
        (tender_id, page_url, failed_type, page_num, page_type, publish_date)
        VALUES
        (%s, %s, %s, %s, %s, %s)"""
        params = (
        self.tender_id, self.page_url, self.failed_type, self.page_num, self.page_type, self.publish_date)

        self.db.execute(command, params)
        return tender_id

    def get_failed_pages(self):
        command = 'SELECT * FROM failed_page WHERE failed_type=%s AND reprocessed = 0'
        params = (self.failed_type,)

        result = self.db.query(command, params)
        return result

    def update_reprocess_status(self):
        command = """UPDATE failed_page 
                SET process_times = process_times + 1, reprocessed = %s, last_process_time = CURRENT_TIMESTAMP
                WHERE
                page_url=%s AND page_num=%s"""
        params = (self.reprocessed, self.page_url, self.page_num)

        self.db.execute(command, params)
