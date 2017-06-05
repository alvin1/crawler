from modules.database_helper import DatabaseHelper


class TrenderInfo(object):
    def __init__(self, tender_id, tender_name, pubdate, page_url, owner, owner_phone, tenderee, tenderee_phone,
                 tenderee_proxy, tenderee_proxy_phone, tender_openning_location, tender_openning_time,
                 tender_ceil_price, publicity_start, publicity_end, other_description, review_department,
                 review_department_phone, administration_department, administration_department_phone):
        self.db = DatabaseHelper()

        self.tender_id = tender_id
        self.tender_name = tender_name
        self.pubdate = pubdate
        self.page_url = page_url
        self.owner = owner
        self.owner_phone = owner_phone
        self.tenderee = tenderee
        self.tenderee_phone = tenderee_phone
        self.tenderee_proxy = tenderee_proxy
        self.tenderee_proxy_phone = tenderee_proxy_phone
        self.tender_openning_location = tender_openning_location
        self.tender_openning_time = tender_openning_time
        self.tender_ceil_price = tender_ceil_price
        self.publicity_start = publicity_start
        self.publicity_end = publicity_end
        self.other_description = other_description
        self.review_department = review_department
        self.review_department_phone = review_department_phone
        self.administration_department = administration_department
        self.administration_department_phone = administration_department_phone

    def get_tender_id(self):
        command = 'SELECT tender_id FROM tender_info WHERE tender_id=%s LIMIT 1'
        params = (self.tender_id,)

        result = self.db.query(command, params)
        if result and len(result['data']) == 1:
            return result['data'][0]['tender_id']

        return None

    def save(self):
        tender_id = self.get_tender_id()
        if tender_id is not None:
            return tender_id

        command = """INSERT INTO tender_info 
        (tender_id, tender_name, pubdate, page_url, owner, owner_phone, tenderee, tenderee_phone, tenderee_proxy, 
        tenderee_proxy_phone, tender_openning_location, tender_openning_time, tender_ceil_price, publicity_start,
        publicity_end, other_description, review_department, review_department_phone, administration_department,
        administration_department_phone)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (
        self.tender_id, self.tender_name, self.pubdate, self.page_url, self.owner, self.owner_phone, self.tenderee,
        self.tenderee_phone,
        self.tenderee_proxy, self.tenderee_proxy_phone, self.tender_openning_location,
        self.tender_openning_time,
        self.tender_ceil_price, self.publicity_start, self.publicity_end, self.other_description,
        self.review_department,
        self.review_department_phone, self.administration_department, self.administration_department_phone)

        self.db.execute(command, params)
        return tender_id
