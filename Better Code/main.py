from manage_books import BookManager, SimpleBookSearchStrategy, AdvancedBookSearchStrategy
from manage_users import UserManager, SimpleUserSearch
from manage_checkouts import CheckoutManager
import sys

def print_menu():
    print("\nLibrary Management System")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Add a user")
    print("5. Search for a user")
    print("6. Checkout a book")
    print("7. Return a book")
    print("8. Display checkout history")
    print("9. Exit")

import re

def validate_email(email):
    """
    Validates the email format
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def validate_dob(dob):
    """
    Validates the date of birth format (YYYY-MM-DD)
    """
    dob_regex = r'^\d{4}-\d{2}-\d{2}$'
    return re.match(dob_regex, dob)

def main():
    book_manager = BookManager()
    user_manager = UserManager()
    checkout_manager = CheckoutManager()
    authenticated_user = None

    while True:
        if authenticated_user is None:
            print("\nWelcome to the Library Management System!")
            login_choice = input("Do you have an account? (yes/no): ").lower()
            if login_choice == "yes":
                email = input("Enter your email: ")
                if not validate_email(email):
                    print("Invalid email format. Please enter a valid email.")
                    continue
                user = user_manager.search_users(email, SimpleUserSearch())
                if user:
                    authenticated_user = user[0]
                    print(f"Welcome back, {authenticated_user.name}!")
                else:
                    print("User not found. Please try again.")
                    continue
            elif login_choice == "no":
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                if not validate_email(email):
                    print("Invalid email format. Please enter a valid email.")
                    continue
                dob = input("Enter your date of birth (YYYY-MM-DD): ")
                if not validate_dob(dob):
                    print("Invalid date of birth format. Please enter a valid date in YYYY-MM-DD format.")
                    continue
                authenticated_user = user_manager.add_user(name, email, dob)
                print(f"Welcome, {name}! Your account has been created successfully.")
            else:
                print("Invalid choice.")
                continue

        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            if authenticated_user:
                title = input("Enter the title of the book: ")
                author = input("Enter the author of the book: ")
                isbn = input("Enter the ISBN of the book: ")
                book_manager.add_book(title, author, isbn)
            else:
                print("Please log in or create an account to add a book.")

        elif choice == "2":
            if authenticated_user:
                isbn = input("Enter the ISBN of the book to remove: ")
                book_manager.remove_book(isbn)
            else:
                print("Please log in or create an account to remove a book.")

        elif choice == "3":
            query = input("Enter your search query: ")
            search_strategy = input("Enter search strategy (simple/advanced): ").lower()
            if search_strategy == "simple":
                books = book_manager.search_book(query, SimpleBookSearchStrategy())
            elif search_strategy == "advanced":
                books = book_manager.search_book(query, AdvancedBookSearchStrategy())
            else:
                print("Invalid search strategy.")
                continue
            if books:
                for book in books:
                    print(book)
            else:
                print("No matching books found.")

        elif choice == "4":
            if authenticated_user:
                print("You are already logged in.")
            else:
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                if not validate_email(email):
                    print("Invalid email format. Please enter a valid email.")
                    continue
                dob = input("Enter your date of birth (YYYY-MM-DD): ")
                if not validate_dob(dob):
                    print("Invalid date of birth format. Please enter a valid date in YYYY-MM-DD format.")
                    continue
                authenticated_user = user_manager.add_user(name, email, dob)
                print(f"Welcome, {authenticated_user.name}! Your account has been created successfully.")

        elif choice == "5":
            if authenticated_user:
                query = input("Enter your search query: ")
                users = user_manager.search_users(query, SimpleUserSearch())
                if users:
                    for user in users:
                        print(user.__dict__)
                else:
                    print("No matching users found.")
            else:
                print("Please log in or create an account to search for a user.")

        elif choice == "6":
            if authenticated_user:
                isbn = input("Enter the ISBN of the book to checkout: ")
                book = next((b for b in book_manager.books if b.isbn == isbn), None)
                if book:
                    checkout_manager.checkout_book(authenticated_user, book)
                else:
                    print("Book not found.")
            else:
                print("Please log in or create an account to checkout a book.")

        elif choice == "7":
            if authenticated_user:
                isbn = input("Enter the ISBN of the book to return: ")
                book = next((b for b in book_manager.books if b.isbn == isbn), None)
                if book:
                    checkout_manager.return_book(authenticated_user, book)
                else:
                    print("Book not found.")
            else:
                print("Please log in or create an account to return a book.")

        elif choice == "8":
            history = checkout_manager.get_checkout_history()
            if history:
                for checkout in history:
                    print(f"User: {checkout.user.name}, Book: {checkout.book.title}, Checkout Date: {checkout.checkout_date}, Return Date: {checkout.return_date}")
            else:
                print("No checkout history found.")

        elif choice == "9":
            print("Exiting the program.")
            sys.exit()

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
