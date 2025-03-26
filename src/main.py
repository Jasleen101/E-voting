import random
from abc import ABC, abstractmethod

class User:
    def __init__(self, email, password, first_name, user_role):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.user_role = user_role

    def __repr__(self):
        return f"User(email='{self.email}', first_name='{self.first_name}', user_role='{self.user_role}')"


class Voter(User):
    def __init__(self, email, password, first_name, is_authenticated):
        super().__init__(email, password, first_name, 'Voter')
        self.is_authenticated = is_authenticated
        self.has_voted = False

    def cast_a_vote(self):
        if not self.has_voted:
            self.has_voted = True
            return True
        else:
            raise Exception("Voter has already casted their vote!")

    def cancel_vote(self):
        if self.has_voted:
            self.has_voted = False
            return True
        else:
            raise Exception("Voter has not casted their vote yet!")
        

class Admin(User):

    def __init__(self, email, password, first_name):
        super().__init__(email, password, first_name, 'Admin')

    def __repr__(self):
        return f"Admin(email={self.email}, first_name={self.first_name}, user_role={self.user_role})"


class Candidate(User):
    def __init__(self, email, password, first_name, candidate_id, candidate_name, candidate_party):
        super().__init__(email, password, first_name, 'Candidate')
        self.candidate_id = candidate_id
        self.candidate_name = candidate_name
        self.candidate_party = candidate_party
        self.votes = 0
        self.nominated = False

    def __repr__(self):
        return f"Candidate(email='{self.email}', first_name='{self.first_name}', candidate_id='{self.candidate_id}', candidate_name='{self.candidate_name}', candidate_party='{self.candidate_party}')"

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


class Election:
    def __init__(self, election_name, election_start_date, election_end_date):
        self.election_name = election_name
        self.election_start_date = election_start_date
        self.election_end_date = election_end_date
        self.voters = []
        self.candidates = []
        self.voting_strategy = None

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
            selected_candidates = self.voting_strategy.vote(voter, self.candidates)
            for candidate in selected_candidates:
                candidate.receive_vote()


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


class VotingSystem:
    def calculate_votes(self, candidates):
        return {candidate.candidate_name: candidate.votes for candidate in candidates}

    def determine_winner(self, candidates):
        winner = max(candidates, key=lambda x: x.votes)
        return winner

class VotingStrategy(ABC):

    @abstractmethod
    def vote(self, voter, candidates):
        pass

class SingleTransferableStrategy(VotingStrategy):
    """
    Ranking the options from 1,2,3 etc
    Strategy: Ranking the options from 1, 2, 3, etc.
    Summary: Allows voters to choose candidates in order of preference, with each candidate assigned a numerical rank.
    Purpose: Facilitates the selection of multiple candidates, enabling voters to express their preferences comprehensively.
    """
    def vote(self, voter, candidates):
        print("Choose candidates in order of preference:")
        selected_candidates = []
        for i, candidate in enumerate(candidates):
            # Prompt the user to select candidates using buttons or checkboxes in a web UI
            print(f"{i+1}. {candidate.candidate_name}")
            # In a web UI, the user would click on buttons or checkboxes to select candidates
            choice = input(f"Select {candidate.candidate_name}? (Y/N): ").lower()
            if choice == 'y':
                selected_candidates.append(candidate)
        return selected_candidates

class FirstPastThePostStrategy(VotingStrategy):
    """
    Only choose one option
    Strategy: Only choose one option.
    Summary: Requires voters to select only one candidate, typically their top choice.
    Purpose: Simple and straightforward, ideal for single-winner elections where the candidate with the most votes wins.
    """
    def vote(self, voter, candidates):
        print("Choose one candidate:")
        for i, candidate in enumerate(candidates):
            # Prompt the user to select a candidate using buttons or checkboxes in a web UI
            print(f"{i+1}. {candidate.candidate_name}")
        # In a web UI, the user would click on a button or checkbox to select a candidate
        choice = int(input("Enter the number corresponding to your chosen candidate: "))
        return [candidates[choice - 1]]

class PreferentialVotingStrategy(VotingStrategy):
    """
    Voters rank candidates in order of preference.
    Strategy: Voters rank candidates in order of preference.
    Summary: Enables voters to rank candidates according to their preferences, allowing for nuanced expression of support.
    Purpose: Particularly useful in elections with multiple rounds or when selecting from a field of candidates, helping to identify the most broadly acceptable candidate.
    """
    def vote(self, voter, candidates):
        print("Rank candidates in order of preference:")
        ranked_candidates = []
        # Prompt the user to rank candidates
        for i, candidate in enumerate(candidates):
            rank = int(input(f"Rank {candidate.candidate_name} (1 for first preference, 2 for second, etc.): "))
            ranked_candidates.append((candidate, rank))
        # Sort candidates based on ranks
        ranked_candidates.sort(key=lambda x: x[1])
        # Return the sorted list of candidates
        return [candidate[0] for candidate in ranked_candidates]

if __name__ == "__main__":
    # Creating sample instances
    voter1 = Voter("voter1@example.com", "password", "John", True)
    voter2 = Voter("voter2@example.com", "password", "Alice", True)
    candidate1 = Candidate("candidate1@example.com", "password", "Michael", 1, "Michael Smith", "Independent")
    candidate2 = Candidate("candidate2@example.com", "password", "Emma", 2, "Emma Johnson", "Democratic")

    # Creating an election
    election = Election("Presidential Election", "2024-04-01", "2024-04-30")
    election.add_voter(voter1)
    election.add_voter(voter2)
    election.add_candidate(candidate1)
    election.add_candidate(candidate2)

    # Submit nomination for candidate1 and candidate2
    candidate1.submitNomination()
    candidate2.submitNomination()

    # Cancel nomination for candidate2
    candidate2.cancelNomination()

    # Defining a voting strategy (replace with the desired strategy)
    election.set_voting_strategy(FirstPastThePostStrategy())

    # Conducting the election
    election.conduct_election()

    # Creating a VotingSystem instance
    voting_system = VotingSystem()

    # Calculating votes and determining the winner
    votes = voting_system.calculate_votes(election.candidates)
    winner = voting_system.determine_winner(election.candidates)

    # Creating a CastVote instance
    cast_vote = CastVote()

    # Submitting and canceling votes
    cast_vote.submit_vote(voter1)
    cast_vote.cancel_vote(voter2)

    # Printing the results
    print("Total Votes:", votes)
    print("Winner:", winner.candidate_name)
