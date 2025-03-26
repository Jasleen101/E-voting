"""
calculate votes and returns winner
"""
from voting_strategy import FirstPastThePostStrategy, SingleTransferableStrategy, PreferentialVotingStrategy

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
