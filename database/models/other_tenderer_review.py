from modules.database import DatabaseHelper


class CandidateProjects(object):
    def __init__(self, tender_id, tenderer_name, price_or_vote_down, price_review_or_vote_down_reason,
                 review_score_or_description):
        self.tender_id = tender_id
        self.tenderer_name = tenderer_name
        self.price_or_vote_down = price_or_vote_down
        self.price_review_or_vote_down_reason = price_review_or_vote_down_reason
        self.review_score_or_description = review_score_or_description

    def save(self):
        command = """INSERT INTO other_tenderer_review 
        (tender_id, tenderer_name, price_or_vote_down, price_review_or_vote_down_reason, review_score_or_description)
        VALUES
        (%s, %s, %s, %s, %s)"""
        params = (self.tender_id, self.tenderer_name, self.price_or_vote_down, self.price_review_or_vote_down_reason,
                  self.review_score_or_description)

        db = DatabaseHelper()
        db.execute(command, params)
