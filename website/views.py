"""
This file store the standard root pages of our website
"""
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, make_response, request
from flask_login import login_required, current_user
from .models import Note, User, Election, Candidate, CastVote
from . import db
import json
from datetime import datetime
import pandas as pd
from io import BytesIO
import sys
import os
# Get the path of the directory containing main5.py
main5_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(main5_dir)
from src.main5 import Election as ElectionOOP, VotingStrategyFactory, FirstPastThePostStrategy, SingleTransferableStrategy, PreferentialVotingStrategy

# Blueprint is a template for the web application and helps to break down to smaller componments
views = Blueprint('views', __name__)

# define a vie and the / allow you to navigate to the main page
@views.route('/', methods=['GET', 'POST'])

#admin home
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note') #Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/voter-home-page')
@login_required
def voter_home():
    return render_template("voter_home_page.html", user=current_user)

@views.route('/candidate-home-page')
@login_required
def candidate_home():
    return render_template("candidate_home_page.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/users-list')
def users_list():
    users = User.query.with_entities(User.id, User.first_name, User.email, User.user_role).all()
    return render_template("users_list.html", users=users, user=current_user)

@views.route('/add-election', methods=['GET', 'POST'])
@login_required
def add_election():
    if request.method == 'POST':
        election_name = request.form.get('election_name')
        election_start_date_str = request.form.get('election_start_date')
        election_end_date_str = request.form.get('election_end_date')
        voting_strategy_type = request.form.get('choose_voting_strategy')

        # Validate the input
        if not election_name or not election_start_date_str or not election_end_date_str or not voting_strategy_type:
            flash('Please fill out all fields', category='error')
        else:
            # Convert date strings to datetime objects
            election_start_date = datetime.strptime(election_start_date_str, '%Y-%m-%dT%H:%M')
            election_end_date = datetime.strptime(election_end_date_str, '%Y-%m-%dT%H:%M')

            # Create a new election object
            new_election = ElectionOOP(election_name=election_name, election_start_date=election_start_date, election_end_date=election_end_date)
            new_election_db = Election(election_name=election_name, election_start_date=election_start_date, election_end_date=election_end_date, voting_strategy=voting_strategy_type)

            # set voting strategy
            if voting_strategy_type == 'FirstPastThePost':
                new_election.set_voting_strategy(FirstPastThePostStrategy())
            elif voting_strategy_type == 'SingleTransferable':
                new_election.set_voting_strategy(SingleTransferableStrategy())
            elif voting_strategy_type == 'PreferentialVoting':
                new_election.set_voting_strategy(PreferentialVotingStrategy())
            else:
                flash('Invalid voting strategy selected', category='error')
                return redirect(url_for('views.add_election'))
            
            db.session.add(new_election_db)
            db.session.commit()
            
            flash('New election added successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template("new_election.html", user=current_user)

@views.route('/elections-list')
@login_required
def elections_list():
    elections = Election.query.all()
    return render_template("elections_list.html", user=current_user, elections=elections)

@views.route('/view-results')
@login_required
def view_results():
    return render_template("view_results.html")

@views.route('/submit-nomination', methods=['GET', 'POST'])
@login_required
def submit_nomination():
    if request.method == 'POST':
        election_id = request.form.get('election')
        candidate_name = request.form.get('candidate_name')
        candidate_party = request.form.get('candidate_party')
        constituency = request.form.get('constituency')

        # Validate the input
        if not election_id or not candidate_name or not candidate_party or not constituency:
            flash('Please fill out all fields', category='error')
        else:
            # Check if the election exists
            election = Election.query.get(election_id)
            if not election:
                flash('Invalid election selected', category='error')
            else:
                # Create a new candidate object
                new_candidate = Candidate(candidate_name=candidate_name, candidate_party=candidate_party,
                                          constitute=constituency, election_id=election_id)
                db.session.add(new_candidate)
                db.session.commit()
                flash('Nomination submitted successfully!', category='success')
                return redirect(url_for('views.home'))

    # Fetch running elections for the dropdown
    running_elections = Election.query.all()
    return render_template("submit_nomination.html", user=current_user, running_elections=running_elections)

@views.route('/cancel-nomination', methods=['GET', 'POST'])
@login_required
def cancel_nomination():
    current_user_candidate = None  # Initialize the variable

    # Check if the current user is a candidate
    if current_user.user_role == 'Candidate':
        # Get the candidate object for the current user
        current_user_candidate = Candidate.query.filter_by(email=current_user.email).first()

    return render_template("cancel_nomination.html", user=current_user, current_user_candidate=current_user_candidate)


# Handles the selection of voting method
@views.route('/select-voting-method', methods=['GET', 'POST'])
@login_required
def select_voting_method():
    if request.method == 'POST':
        voting_method = request.form.get('voting_method')

        if voting_method == 'in_booth':
            flash('In Booth voting is not available.', category='error')
            return redirect(url_for('views.voter_home'))
        elif voting_method == 'online_voting':
            return redirect(url_for('views.vote'))
    
    # Logic for rendering the select_voting_method.html template for GET requests
    return render_template("vote_page.html", user=current_user)

# Function to check if an election is ongoing
def election_is_ongoing(election):
    current_date = datetime.now()
    return election.election_start_date <= current_date <= election.election_end_date

# Modify the /vote endpoint to render a page with the list of ongoing elections
@views.route('/vote')
@login_required
def vote():
    # Fetch all elections
    all_elections = Election.query.all()

    # Filter ongoing elections using list comprehension
    ongoing_elections = [election for election in all_elections if election_is_ongoing(election)]

    return render_template("vote_elections_list.html", user=current_user, elections=ongoing_elections)

@views.route('/election-vote', methods=['GET', 'POST'])
@login_required
def election_vote():
    if request.method == 'POST':
        # Handle form submission
        # Determine the selected election and its voting strategy
        election_id = request.form.get('election_id')
        election = Election.query.get(election_id)

        if election:
            if election.voting_strategy == 'PreferentialVoting':
                return redirect(url_for('views.preferential_vote', election_id=election_id))
            elif election.voting_strategy == 'SingleTransferable':
                return redirect(url_for('views.single_transferable_vote', election_id=election_id))
            elif election.voting_strategy == 'FirstPastThePost':
                return redirect(url_for('views.first_past_the_post_vote', election_id=election_id))
            else:
                flash('Invalid voting strategy for the selected election', category='error')
                return redirect(url_for('views.election_vote'))
        else:
            flash('Invalid election selected', category='error')
            return redirect(url_for('views.election_vote'))

    # Fetch all ongoing elections
    all_elections = Election.query.all()
    ongoing_elections = [election for election in all_elections if election_is_ongoing(election)]


    return render_template("election_vote_page.html", user=current_user, elections=ongoing_elections)

# 3 routes for the voting strategies
# Separate page for online voting
@views.route('/preferential-vote', methods=['GET', 'POST'])
@login_required
def preferential_vote():
    if request.method == 'POST':
        # Check if the user has already voted for this election
        election_id = request.args.get('election_id')
        existing_vote = CastVote.query.filter_by(election_id=election_id, voter_id=current_user.id).first()
        if existing_vote:
            flash('You have already voted for this election.', category='error')
            return redirect(url_for('views.voter_home'))

        # Fetch candidates for the current election
        candidates = Candidate.query.filter_by(election_id=election_id).all()

        # Process the vote
        ranked_candidates = []
        for candidate in candidates:
            rank = int(request.form.get(f'candidate_rank_{candidate.candidate_id}'))
            ranked_candidates.append((candidate, rank))
        ranked_candidates.sort(key=lambda x: x[1])

        # Save the vote in the database
        new_vote = CastVote(voter_id=current_user.id, election_id=election_id, ranked_candidates=ranked_candidates)
        db.session.add(new_vote)
        db.session.commit()

        flash('Your vote has been recorded successfully.', category='success')
        return redirect(url_for('views.voter_home'))
    
    else:
        # Fetch candidates for the current election
        current_election_id = request.args.get('election_id')
        candidates = Candidate.query.filter_by(election_id=current_election_id).all()

        return render_template("preferential_vote.html", user=current_user, candidates=candidates)




@views.route('/single-transferable-vote', methods=['GET', 'POST'])
@login_required
def single_transferable_vote():
    current_election_id = request.args.get('election_id')
    candidates = Candidate.query.filter_by(election_id=current_election_id).all()
    return render_template("single_transferable_vote.html", user=current_user, candidates=candidates)

@views.route('/first-past-the-post-vote', methods=['GET', 'POST'])
@login_required
def first_past_the_post_vote():
    if request.method == 'POST':
        candidate_id = request.form.get('candidate_id')
        election_id = request.args.get('election_id')

        already_voted = CastVote.query.filter_by(election_id=election_id, voter_id=current_user.id).first()
        if already_voted:
            flash('You have already voted for this election.', category='error')
            return redirect(url_for('views.voter_home'))

        # Save the vote in the database
        new_vote = CastVote(voter_id=current_user.id, candidate_id=candidate_id, election_id=election_id)
        db.session.add(new_vote)
        db.session.commit()

        flash('Your vote has been recorded successfully.', category='success')
        return redirect(url_for('views.voter_home'))

    else:
        current_election_id = request.args.get('election_id')
        candidates = Candidate.query.filter_by(election_id=current_election_id).all()
        return render_template("first_past_the_post.html", user=current_user, candidates=candidates)

@views.route('/generate-excel-report', methods=['GET', 'POST'])
@login_required
def generate_excel_report():
    # Fetch all candidates from the database
    candidates = Candidate.query.all()

    # Prepare candidate data for Excel report
    candidate_data = []
    for candidate in candidates:
        candidate_data.append({
            'ID': candidate.candidate_id,
            'Name': candidate.candidate_name,
            'Party': candidate.candidate_party,
            'Constituency': candidate.constitute,
            'Election ID': candidate.election_id
        })

    # Create a DataFrame from the candidate data
    candidates_df = pd.DataFrame(candidate_data)

    # Create a BytesIO object to hold the Excel file
    excel_file = BytesIO()

    # Write the DataFrame to the BytesIO object as an Excel file
    candidates_df.to_excel(excel_file, index=False)

    # Set the file pointer to the beginning of the BytesIO object
    excel_file.seek(0)

    # Create a Flask response object
    response = make_response(excel_file.getvalue())

    # Set the appropriate content type and attachment filename
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=candidates_report.xlsx'

    return response
