import unittest
from datetime import datetime
import sys

# Add the parent directory of 'tests' to the Python path
sys.path.append('../')

# Now, imports should work relative to the parent directory
from src.main5 import *

# To run the tests in cmd: 
# python -m unittest test_voting_system.py

class TestVotingSystem(unittest.TestCase):
    
    def setUp(self):
        # Initialize test data
        self.voter = Voter("voter@example.com", generate_password_hash("password"), "John", True)
        self.candidate = Candidate("candidate1@example.com", generate_password_hash("password"), "Jasleen", 1, "Jasleen k", "Independent", "Constituency A")
        self.election = Election("Test Election", datetime.now(), datetime.now())
        self.election.add_voter(self.voter)
        self.election.add_candidate(self.candidate)
        self.voting_system = VotingSystem()

    def test_enqueue_dequeue(self):
        # Test enqueue and dequeue operations
        queue = Queue()
        queue.enqueue(1)
        queue.enqueue(2)
        self.assertEqual(queue.size(), 2)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)
        self.assertTrue(queue.is_empty())

    def test_add_voter(self):
        # Test adding a voter to the election
        self.assertEqual(self.election.voters.size(), 1)
        self.assertEqual(self.election.voters.peek(), self.voter)

    def test_add_candidate(self):
        # Test adding a candidate to the election
        self.assertEqual(len(self.election.candidates), 1)
        self.assertEqual(self.election.candidates[0], self.candidate)

    def test_voting_strategy(self):
        # Test setting and conducting an election with a voting strategy
        self.election.set_voting_strategy(FirstPastThePostStrategy())
        self.assertIsInstance(self.election.voting_strategy, FirstPastThePostStrategy)
        self.election.conduct_election()
        # Add assertions for expected behavior or results


    def test_voting_system_singleton(self):
        # Test the singleton behavior of the VotingSystem class
        voting_system_1 = VotingSystem()
        voting_system_2 = VotingSystem()
        self.assertIs(voting_system_1, voting_system_2)

    def test_cast_vote(self):
        # Test casting a vote
        cast_vote = CastVote()
        self.assertTrue(cast_vote.submit_vote(self.voter))
        self.assertFalse(cast_vote.submit_vote(self.voter))  # Attempt to vote again should fail

    def test_cancel_vote(self):
        # Test canceling a vote
        cast_vote = CastVote()
        cast_vote.submit_vote(self.voter)
        self.assertTrue(cast_vote.cancel_vote(self.voter))
        self.assertFalse(cast_vote.cancel_vote(self.voter))  # Attempt to cancel again should fail

if __name__ == '__main__':
    unittest.main()
