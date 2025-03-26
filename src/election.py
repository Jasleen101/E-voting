"""
Running election: who votes for them and candidates running for 
"""

from . import db
from .voting_strategy import FirstPastThePostStrategy
from .queue import Queue
from .voting_system import VotingSystem

"""
class Election:
    def __init__(self,election_name,election_start_date,election_end_date):
        self.election_name = election_name
        self.election_start_date = election_start_date
        self.election_end_date = election_end_date
        self.voters = []
        self.candidates = []

    def add_voter(self, voter):
        self.voters.append(voter)
    
    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def set_voting_strategy(self, voting_strategy):
        self.voting_strategy = voting_strategy

    def conduct_election(self):
        if not self.voting_strategy:
            print("No voting strategy selected. Please set the voting strategy.")
            return

        for voter in self.voters:
            candidate = self.voting_strategy.vote(voter, self.candidates)
            candidate.receive_vote()

            """

class Election:
    def __init__(self, election_name, election_start_date, election_end_date):
        self.election_name = election_name
        self.election_start_date = election_start_date
        self.election_end_date = election_end_date
        self.voters = Queue()  # Initialize the voter queue
        self.candidates = []
        self.voting_strategy = None

    def add_voter(self, voter):
        self.voters.enqueue(voter)  # Add voter to the queue

    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def set_voting_strategy(self, voting_strategy):
        self.voting_strategy = voting_strategy

    def conduct_election(self):
        if not self.voting_strategy:
            print("No voting strategy selected. Please set the voting strategy.")
            return

        while not self.voters.is_empty():  # Continue until all voters have cast their votes
            voter = self.voters.dequeue()  # Get the next voter from the queue
            selected_candidates = self.voting_strategy.vote(voter, self.candidates)
            for candidate in selected_candidates:
                candidate.receive_vote()

        VotingSystem().notify_observers()
