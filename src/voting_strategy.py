"""
Type of voting:

First past the post strategy
Preferential Voting Strategy
single transferable votes

Strategy Pattern (Support for Multiple Voting Mechanisms):
"""
from abc import ABC, abstractmethod

# Strategy Design Pattern
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
            print(f"{i+1}. {candidate.candidate_name}")
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
            print(f"{i+1}. {candidate.candidate_name}")
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
        for i, candidate in enumerate(candidates):
            rank = int(input(f"Rank {candidate.candidate_name} (1 for first preference, 2 for second, etc.): "))
            ranked_candidates.append((candidate, rank))
        ranked_candidates.sort(key=lambda x: x[1])
        return [candidate[0] for candidate in ranked_candidates]
