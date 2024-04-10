from uuid import uuid4
from datetime import datetime

class User:
    def __init__(self, email, name, dob, user_id=None, joining_date=None) -> None:
        self.user_id = user_id or str(uuid4())
        self.email = email
        self.name = name
        self.dob = dob
        self.joining_date = joining_date or datetime.now().date()
        self.books_borrowed = 0
        self.active_books = 0
        self.borrow_limit = 3
    
    def add_active_book(self):
        self.books_borrowed += 1
        self.active_books += 1
    
    def dcr_active_book(self):
        if self.active_books > 0:
            self.active_books -=1

    def has_reached_limit(self):
        if self.active_books >= self.borrow_limit:
            return True
    
        return False

    def modify_borrow_limit(self, number:int):
        self.borrow_limit = number

class UserBuilder:
    def __init__(self, email, name, dob):
        self.email = email
        self.name = name
        self.dob = dob
        self.user_id = None
        self.joining_date = None

    def set_user_id(self, user_id):
        self.user_id = user_id
        return self

    def set_joining_date(self, joining_date):
        self.joining_date = joining_date
        return self

    def build(self):
        return User(
            email=self.email,
            name=self.name,
            dob=self.dob,
            user_id=self.user_id,
            joining_date=self.joining_date
        )
    
class UserSearch:
    def search(self, users, query):
        raise NotImplementedError

class SimpleUserSearch(UserSearch):
    def search(self, users, query):
        results = []
        for user in users:
            if query.lower() in user.name.lower() or query.lower() in user.email.lower():
                results.append(user)
        return results
    
# Compatible with Advanced Search Strategies, too

class UserManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.users = []
        return cls._instance

    def add_user(self, name, email, dob):
        user = UserBuilder(email, name, dob).build()
        self.users.append(user)
        return user
        print("User added successfully")

    def search_users(self, query, search_strategy):
        return search_strategy.search(self.users, query)
