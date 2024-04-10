from datetime import datetime

class Checkout:
    """
    Represents a single checkout instance
    """
    def __init__(self, user, book, checkout_date=None, return_date=None):
        self.user = user # User Object
        self.book = book # Book Object
        self.checkout_date = checkout_date or datetime.now()
        self.return_date = return_date

    def return_book(self):
        """
        Marks the book as returned and sets the return date
        """
        if self.return_date is None:
            self.return_date = datetime.now()
            return True
        return False

class CheckoutHistory:
    """
    Keeps track of checkout history
    """
    def __init__(self):
        self.history = []

    def add_to_history(self, checkout):
        """
        Adds a checkout instance to the history
        """
        self.history.append(checkout)

class CheckoutManager:
    """
    Manages all checkouts
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.checkouts = []
            cls._instance.history = CheckoutHistory()
        return cls._instance

    def checkout_book(self, user, book) -> bool:
        """Checkout a book

        Args:
            user (User): User object
            book (Book): Book object
        """
        # Ensure Transaction Atomicity
        try:
            # Check if book is available or not
            if not book.available:
                print(f"Book {book.title} with ISBN {book.isbn} not available for checkout")
                return False

            if user.has_reached_limit():
                print(f"User {user.name} has borrowed too many books.")
                return False

            # Create a checkout instance
            checkout_instance = Checkout(user, book)
            # Add it to user's active books list
            user.add_active_book()
            # Log it
            self.checkouts.append(checkout_instance)
            self.history.add_to_history(checkout_instance)
            # Book is no longer available
            book.set_availability(False)
            # print the message
            print("Book checked out successfully")
            return True
        except Exception as e:
            # If an error occurs, rollback changes
            if checkout_instance in self.checkouts:
                self.checkouts.remove(checkout_instance)
            if checkout_instance in self.history.history:
                self.history.history.remove(checkout_instance)
            if not book.available:
                book.set_availability(True)
            if user.has_reached_limit():
                user.dcr_active_book()
            print(f"An error occurred during checkout: {e}")
            return False

    def return_book(self, user, book) -> bool:
        """Return a book

        Args:
            user (User): User object
            book (Book): Book object
        """
        try:
            for checkout in self.checkouts:
                if checkout.user.user_id == user.user_id and checkout.book.isbn == book.isbn:
                    # return the book
                    return_status = checkout.return_book()
                    # Check if already returned or not
                    if not return_status:
                        print("Book already returned")
                        return False

                    # Decrement user's active books list
                    user.dcr_active_book()
                    # set availability of book
                    book.set_availability(True)
                    print("Book returned successfully!")
                    return True

            print("No matching checkout found for the user and book combination")
            return False
        except Exception as e:
            print(f"An error occurred during return: {e}")
            return False

    def get_checkout_history(self):
        """
        Returns the checkout history
        """
        return self.history.history
