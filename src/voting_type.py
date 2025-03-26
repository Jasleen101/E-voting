"""
Type of voting: in person or online
#bridge pattern
"""

from abc import ABC, abstractmethod

# Implementor Interface
class VotingInterface(ABC):
    @abstractmethod
    def vote(self, voter, candidate):
        pass

# Concrete Implementor 1
class InPersonVoting(VotingInterface):
    def vote(self, voter, candidate):
        # Implementation for in-person voting
        pass

# Concrete Implementor 2
class OnlineVoting(VotingInterface):
    def vote(self, voter, candidate):
        # Implementation for online voting
        pass