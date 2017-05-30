from modules.database import DatabaseHelper


class Candidate(object):
    def __init__(self, tender_id, candidate_id, ranking, candidate_name, tender_price, tender_price_review,
                 review_score):
        self.tender_id = tender_id
        self.candidate_id = candidate_id
        self.ranking = ranking
        self.candidate_name = candidate_name
        self.tender_price = tender_price
        self.tender_price_review = tender_price_review
        self.review_score = review_score

    def save(self):
        command = """INSERT INTO candidate 
        (tender_id, candidate_id, ranking, candidate_name, tender_price, tender_price_review, review_score)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)"""
        params = (self.tender_id, self.candidate_id, self.ranking, self.candidate_name, self.tender_price,
                  self.tender_price_review,
                  self.review_score)

        db = DatabaseHelper()
        db.execute(command, params)
