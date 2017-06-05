from modules.database_helper import DatabaseHelper


class Candidate(object):
    def __init__(self, tender_id, ranking, candidate_name, tender_price, tender_price_review, review_score,
                 candidate_id=None):
        self.db = DatabaseHelper()

        self.tender_id = tender_id
        self.candidate_id = candidate_id
        self.ranking = ranking
        self.candidate_name = candidate_name
        self.tender_price = tender_price
        self.tender_price_review = tender_price_review
        self.review_score = review_score

    def get_candidate_id(self):
        command = 'SELECT candidate_id FROM candidate WHERE tender_id=%s AND candidate_name=%s LIMIT 1'
        params = (self.tender_id, self.candidate_name,)

        result = self.db.query(command, params)
        if result and len(result['data']) == 1:
            return result['data'][0]['candidate_id']

        return None

    def save(self):
        candidate_id = self.get_candidate_id()
        if candidate_id is not None:
            return candidate_id

        self.candidate_id = self.db.generate_id()
        command = """INSERT INTO candidate 
        (tender_id, candidate_id, ranking, candidate_name, tender_price, tender_price_review, review_score)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)"""
        params = (self.tender_id, self.candidate_id, self.ranking, self.candidate_name, self.tender_price,
                  self.tender_price_review,
                  self.review_score)

        self.db.execute(command, params)
        return self.candidate_id
