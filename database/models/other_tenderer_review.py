from modules.database_helper import DatabaseHelper


class OtherTendererReview(object):
    def __init__(self, tender_id, tenderer_name, price_or_vote_down, price_review_or_vote_down_reason,
                 review_score_or_description, tenderer_id=None):
        self.db = DatabaseHelper()

        self.tender_id = tender_id
        self.tenderer_id = tenderer_id
        self.tenderer_name = tenderer_name
        self.price_or_vote_down = price_or_vote_down
        self.price_review_or_vote_down_reason = price_review_or_vote_down_reason
        self.review_score_or_description = review_score_or_description

    def get_tenderer_id(self):
        command = 'SELECT tenderer_id FROM other_tenderer_review WHERE tender_id=%s AND tenderer_name=%s LIMIT 1'
        params = (self.tender_id, self.tenderer_name,)

        result = self.db.query(command, params)
        if result and len(result['data']) == 1:
            return result['data'][0]['tenderer_id']

        return None

    def save(self):
        tenderer_id = self.get_tenderer_id()
        if tenderer_id is not None:
            return tenderer_id

        self.tenderer_id = self.db.generate_id()
        command = """INSERT INTO other_tenderer_review 
        (tender_id, tenderer_id, tenderer_name, price_or_vote_down, price_review_or_vote_down_reason, review_score_or_description)
        VALUES
        (%s, %s, %s, %s, %s, %s)"""
        params = (self.tender_id, self.tenderer_id, self.tenderer_name, self.price_or_vote_down, self.price_review_or_vote_down_reason,
                  self.review_score_or_description)

        self.db.execute(command, params)
        return self.tenderer_id
