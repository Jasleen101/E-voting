# Running all
from src.voter import Voter
from src.candidate import Candidate
from src.election import Election
from src.voting_strategy import FirstPastThePostStrategy
from werkzeug.security import generate_password_hash

if __name__ == "__main__":
    # Creating sample instances
    voter1 = Voter("voter1@example.com", generate_password_hash("password"), "John", True)
    voter2 = Voter("voter2@example.com", generate_password_hash("password"), "Alice", True)
    candidate1 = Candidate("candidate1@example.com", generate_password_hash("password"), "Michael", 1, "Michael Smith", "Independent", "Constituency A")
    candidate2 = Candidate("candidate2@example.com", generate_password_hash("password"), "Emma", 2, "Emma Johnson", "Democratic", "Constituency B")

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
