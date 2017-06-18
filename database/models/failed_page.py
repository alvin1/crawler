from modules.database_helper import DatabaseHelper


class FailedPage(object):
    def __init__(self, tender_id=None, page_url=None, failed_type=None, page_num=None, page_type=None,
                 pubdate=None, reprocessed=None):
        self.db = DatabaseHelper()

        self.tender_id = tender_id
        self.page_url = page_url
        self.failed_type = failed_type
        self.page_num = page_num
        self.page_type = page_type
        self.pubdate = pubdate
        self.reprocessed = reprocessed

    def check_page_existed(self):
        command = 'SELECT * FROM failed_page WHERE page_url=%s AND page_num=%s AND reprocessed = 0 LIMIT 1'
        params = (self.page_url, self.page_num)

        result = self.db.query(command, params)
        if result and len(result['data']) == 1:
            return True
        return False

    def save(self):
        page_existed = self.check_page_existed()
        if page_existed:
            return

        command = """INSERT INTO failed_page 
        (tender_id, page_url, failed_type, page_num, page_type, pubdate)
        VALUES
        (%s, %s, %s, %s, %s, %s)"""
        params = (
        self.tender_id, self.page_url, self.failed_type, self.page_num, self.page_type, self.pubdate)

        self.db.execute(command, params)

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
