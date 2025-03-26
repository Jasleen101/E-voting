from . import db
from .user import User

class Admin(User):
    def __init__(self, email, password, first_name):
        super().__init__(email, password, first_name, 'Admin')

    def __repr__(self):
        return f"Admin(email={self.email}, first_name={self.first_name}, user_role={self.user_role})"