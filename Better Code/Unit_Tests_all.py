import unittest
from manage_books import BookManager, BookSearchStrategy, AdvancedBookSearchStrategy, SimpleBookSearchStrategy, Book
from datetime import datetime
from manage_checkouts import CheckoutManager, Checkout, CheckoutHistory
from manage_users import UserManager, UserBuilder, SimpleUserSearch, User

class TestBookManager(unittest.TestCase):
    def setUp(self):
        self.book_manager = BookManager()

    def test_isbn_checker_valid_isbn10(self):
        # valid    
        isbn = "0132350882" 
        self.assertTrue(self.book_manager._isbn_checker(isbn))

    def test_isbn_checker_invalid_length(self):
        isbn = "01323508"  # Invalid ISBN
        self.assertFalse(self.book_manager._isbn_checker(isbn))

    def test_isbn_checker_invalid_characters(self):
        isbn = "978-0-13-235088-4X"  # Invalid
        self.assertFalse(self.book_manager._isbn_checker(isbn))

    def test_isbn_checker_invalid_checksum(self):
        isbn = "9780132350889"  # Invalid 
        self.assertFalse(self.book_manager._isbn_checker(isbn))
    
    def test_add_book(self):
        # Test adding a book
        self.assertTrue(self.book_manager.add_book("Title1", "Author1", "0596007973"))

        # Test adding a book with existing ISBN
        self.assertFalse(self.book_manager.add_book("Title2", "Author2", "0596007973"))
        self.assertEqual(len(self.book_manager.books), 1)  

    def test_remove_book(self):
        # Test removing a book
        self.book_manager.add_book("Title1", "Author1", "0132350882")
        self.assertTrue(self.book_manager.remove_book("0132350882"))
        self.assertEqual(len(self.book_manager.books), 0)

        # Test removing a non-existing book
        self.assertFalse(self.book_manager.remove_book("978-1-60309-502-0"))

    def test_search_book(self):
        # Test searching for a book
        self.book_manager.add_book("Title1", "Author1", "0132350882")
        self.book_manager.add_book("Title2", "Author2", "0596007973")

        # Test simple search strategy
        found_books = self.book_manager.search_book("Title1")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].title, "Title1")

        # Test no matching books found
        found_books = self.book_manager.search_book("Title3")
        self.assertEqual(len(found_books), 0)

    def test_find_book_by_isbn(self):
        # Test finding a book by ISBN
        self.book_manager.add_book("Title1", "Author1", "0596007973")
        self.book_manager.add_book("Title2", "Author2", "0132350882")

        # Test finding an existing book by ISBN
        found_book = self.book_manager._find_book_by_isbn("0132350882")
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book.title, "Title2")

        # Test finding a non-existing book by ISBN
        found_book = self.book_manager._find_book_by_isbn("1111111111")
        self.assertIsNone(found_book)


class TestCheckoutManager(unittest.TestCase):
    def setUp(self):
        self.checkout_manager = CheckoutManager()

    def test_checkout_book(self):
        user = User("test@example.com", "Test User", "1999-01-01")
        book = Book("Test Book", "Test Author", "1234567890")
        self.assertTrue(self.checkout_manager.checkout_book(user, book))
        self.assertEqual(len(self.checkout_manager.checkouts), 1)
        self.assertIsInstance(self.checkout_manager.checkouts[0], Checkout)
        self.assertEqual(len(self.checkout_manager.history.history), 1)
        self.assertIsInstance(self.checkout_manager.history.history[0], Checkout)

    def test_return_book(self):
        user = User("test@example.com", "Test User", "1990-01-01")
        book = Book("Test Book", "Test Author", "1234567890")
        checkout_instance = Checkout(user, book)
        self.checkout_manager.checkouts.append(checkout_instance)
        self.checkout_manager.history.history.append(checkout_instance)

        # Return the book
        self.assertTrue(self.checkout_manager.return_book(user, book))

        # Test if the return date is set and availability is updated
        self.assertIsNotNone(checkout_instance.return_date)
        self.assertTrue(book.available)

        self.assertEqual(len(self.checkout_manager.checkouts), 2)
        self.assertEqual(user.active_books, 0)
        self.assertEqual(len(self.checkout_manager.history.history), 2)

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()

    def test_add_user(self):
        # Add a user to the user manager
        user = self.user_manager.add_user("Rohan", "rohan@example.com", "1990-01-01")

        # Test if user is added successfully
        self.assertEqual(len(self.user_manager.users), 1)
        self.assertEqual(user.name, "Rohan")
        self.assertEqual(user.email, "rohan@example.com")
        self.assertEqual(user.dob, "1990-01-01")

    def test_search_users(self):
        # Add some users
        self.user_manager.add_user("Rohan", "rohan@example.com", "1990-01-01")
        self.user_manager.add_user("Ashish", "ashish@example.com", "1985-05-15")
        self.user_manager.add_user("Suman", "suman@example.com", "1995-07-20")

        # Test if search is case-insensitive
        search_results = self.user_manager.search_users("rohan", SimpleUserSearch())
        self.assertEqual(len(search_results), 2)
        self.assertEqual(search_results[0].name, "Rohan")

        # Test if search works with email
        search_results = self.user_manager.search_users("ashish@example.com", SimpleUserSearch())
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].name, "Ashish")


if __name__ == '__main__':
    unittest.main()
