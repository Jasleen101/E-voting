from . import db
from .user import User
        
class Candidate(User):
    def __init__(self, email, password, first_name, candidate_id, candidate_name, candidate_party,constituency):
        super().__init__(email, password, first_name, 'Candidate')
        self.candidate_id = candidate_id
        self.candidate_name = candidate_name
        self.candidate_party = candidate_party
        self.constituency = constituency 

        self.votes = 0
        self.nominated = False

    def __repr__(self):
        return f"Candidate(email='{self.email}', first_name='{self.first_name}', candidate_id='{self.candidate_id}', candidate_name='{self.candidate_name}', candidate_party='{self.candidate_party}', constituency='{self.constituency}')"

    def receive_vote(self):
        self.votes += 1

    def submitNomination(self):
        if not self.nominated:
            self.nominated = True
            return True
        else:
            raise Exception("Candidate has already submitted nomination!")

    def cancelNomination(self):
        if self.nominated:
            self.nominated = False
            return True
        else:
            raise Exception("Candidate has not submitted nomination yet!")