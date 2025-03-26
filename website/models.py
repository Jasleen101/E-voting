# from website we are importing db
from . import db
# flask login is module that helps users login
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
#from werkzeug.security import generate_password_hash

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='notes')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    user_role = db.Column(db.String(50), nullable=False, default='User')
    notes = db.relationship('Note', back_populates='user')

class Candidate(db.Model):
    candidate_id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(150))
    candidate_party = db.Column(db.String(150))
    constitute = db.Column(db.String(150))
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'))
    # Relationship with Election to fetch nominations
    election = db.relationship('Election', back_populates='candidates')

class Voter(db.Model):
    voter_id = db.Column(db.Integer, primary_key=True)
    is_authenticated = db.Column(db.Boolean, default=False)

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user = db.relationship('User', back_populates='admin')

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_name = db.Column(db.String(150))
    election_start_date = db.Column(db.DateTime, nullable=False)
    election_end_date = db.Column(db.DateTime, nullable=False)
    winner = db.Column(db.String(150))  
    voting_strategy = db.Column(db.String(150))  
    candidates = db.relationship('Candidate', back_populates='election')

class CastVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voter.voter_id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.candidate_id'), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    voter = db.relationship('Voter', backref='votes')
    candidate = db.relationship('Candidate', backref='votes')
    election = db.relationship('Election', backref='votes')

