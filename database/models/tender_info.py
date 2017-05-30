from modules.database import DatabaseHelper


class TrenderInfo(object):
    def __init__(self, tender_id, tender_name, pubdate, owner, owner_phone, tenderee, tenderee_phone, tenderee_proxy,
                 tenderee_proxy_phone, tender_openning_location, tender_openning_time, tender_ceil_price,
                 publicity_start, publicity_end, other_description, review_department, review_department_phone,
                 administration_department, administration_department_phone):
        self.tender_id = tender_id
        self.tender_name = tender_name
        self.pubdate = pubdate
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

    def save(self):
        command = """INSERT INTO tender_info 
        (tender_id, tender_name, pubdate, owner, owner_phone, tenderee, tenderee_phone, tenderee_proxy, 
        tenderee_proxy_phone, tender_openning_location, tender_openning_time, tender_ceil_price, publicity_start,
        publicity_end, other_description, review_department, review_department_phone, administration_department,
        administration_department_phone)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (self.tender_id, self.tender_name, self.pubdate, self.owner, self.owner_phone, self.tenderee,
                  self.tenderee_phone,
                  self.tenderee_proxy, self.tenderee_proxy_phone, self.tender_openning_location,
                  self.tender_openning_time,
                  self.tender_ceil_price, self.publicity_start, self.publicity_end, self.other_description,
                  self.review_department,
                  self.review_department_phone, self.administration_department, self.administration_department_phone)

        db = DatabaseHelper()
        db.execute(command, params)
