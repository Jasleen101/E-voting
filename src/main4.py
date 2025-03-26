from abc import ABC, abstractmethod
from werkzeug.security import generate_password_hash

# Define the Queue class
class Queue:
    def __init__(self):
        self._items = []

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the item at the front of the queue."""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        return self._items.pop(0)

    def is_empty(self):
        """Return True if the queue is empty, False otherwise."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the queue."""
        return len(self._items)

    def peek(self):
        """Return the item at the front of the queue without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek into an empty queue")
        return self._items[0]

# Singleton Design Pattern
class VotingSystem:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()

    def conduct_election(self):
        if not self.voting_strategy:
            print("No voting strategy selected. Please set the voting strategy.")
            return

        for voter in self.voters:
            selected_candidates = self.voting_strategy.vote(voter, self.candidates)
            for candidate in selected_candidates:
                candidate.receive_vote()

        # Notify observers
        self.notify_observers()

# Factory Method Design Pattern
class VotingStrategyFactory:
    @staticmethod
    def get_strategy(strategy_type):
        if strategy_type == "FirstPastThePost":
            return FirstPastThePostStrategy()
        elif strategy_type == "SingleTransferable":
            return SingleTransferableStrategy()
        elif strategy_type == "PreferentialVoting":
            return PreferentialVotingStrategy()
        else:
            raise ValueError("Invalid strategy type")

# Observer Design Pattern
class Observer(ABC):
    @abstractmethod
    def update(self):
        pass

class LoggingSystem(Observer):
    def update(self):
        print("Election conducted. Logging system updated.")

# Strategy Design Pattern
class VotingStrategy(ABC):
    @abstractmethod
    def vote(self, voter, candidates):
        pass

class SingleTransferableStrategy(VotingStrategy):
    def vote(self, voter, candidates):
        print("Choose candidates in order of preference:")
        selected_candidates = []
        for i, candidate in enumerate(candidates):
            print(f"{i+1}. {candidate.candidate_name}")
            choice = input(f"Select {candidate.candidate_name}? (Y/N): ").lower()
            if choice == 'y':
                selected_candidates.append(candidate)
        return selected_candidates

class FirstPastThePostStrategy(VotingStrategy):
    def vote(self, voter, candidates):
        print("Choose one candidate:")
        for i, candidate in enumerate(candidates):
            print(f"{i+1}. {candidate.candidate_name}")
        choice = int(input("Enter the number corresponding to your chosen candidate: "))
        return [candidates[choice - 1]]

class PreferentialVotingStrategy(VotingStrategy):
    def vote(self, voter, candidates):
        print("Rank candidates in order of preference:")
        ranked_candidates = []
        for i, candidate in enumerate(candidates):
            rank = int(input(f"Rank {candidate.candidate_name} (1 for first preference, 2 for second, etc.): "))
            ranked_candidates.append((candidate, rank))
        ranked_candidates.sort(key=lambda x: x[1])
        return [candidate[0] for candidate in ranked_candidates]

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

if __name__ == "__main__":
    # Creating sample instances
    voter1 = Voter("voter1@example.com", generate_password_hash("password"), "John", True)
    voter2 = Voter("voter2@example.com", generate_password_hash("password"), "Alice", True)
    candidate1 = Candidate("candidate1@example.com", generate_password_hash("password"), "Michael", 1, "Michael Smith", "Independent")
    candidate2 = Candidate("candidate2@example.com", generate_password_hash("password"), "Emma", 2, "Emma Johnson", "Democratic")

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

    # Printing the results
    print("Total Votes:", {candidate.candidate_name: candidate.votes for candidate in election.candidates})
    print("Winner:", max(election.candidates, key=lambda x: x.votes).candidate_name)
