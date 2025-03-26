"""
able to submit and cancel vote, calls the cast_a_vote fuc
"""

class CastVote:
    def submit_vote(self, voter):
        try:
            return voter.cast_a_vote()
        except Exception as e:
            print("Error:", e)
            return False

    def cancel_vote(self, voter):
        try:
            return voter.cancel_vote()
        except Exception as e:
            print("Error:", e)
            return False