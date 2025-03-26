#from website.models import User
from .user import User

"""
class Voter(User):
    
    # inherit from user
    # use super().__init__() to call the constructor of the parent class (User) to initialize the common attributes (email, password, first_name).
    def __init__(self, email, password, first_name, is_authenticated):
        super().__init__(email, password, first_name, 'Voter')
        self.is_authenticated = is_authenticated
        self.has_voted = False
    
    #def __repr__(self):
    #    return f"Voter(id={self.id}, email={self.email}, is_authenticated={self.is_authenticated})"

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

"""

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
        