from . import db

class User(db.Model):
    
    def __init__(self, email, password, first_name,user_role):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.user_role = user_role

    def __repr__(self):
        return f"User(email='{self.email}', first_name='{self.first_name}', user_role='{self.user_role}')"

"""
class User:
    def __init__(self, email, password, first_name, user_role):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.user_role = user_role

    def __repr__(self):
        return f"User(email='{self.email}', first_name='{self.first_name}', user_role='{self.user_role}')"

"""