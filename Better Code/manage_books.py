import re 

class Book:
    """
    Defines a Book
    """
    def __init__(self, title, author, isbn) -> None:
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True

    def __str__(self) -> str:
        """
        Returns:
            str: _description_
        """
        book_string = f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Availability: {self.available}"
        return book_string
    
    def set_availability(self, availability: bool):
        self.available = availability
    
    
class BookBuilder:
    """Builder class for creating Book objects"""
    def __init__(self):
        self.title = None
        self.author = None
        self.isbn = None

    def with_title(self, title):
        self.title = title
        return self

    def with_author(self, author):
        self.author = author
        return self

    def with_isbn(self, isbn):
        self.isbn = isbn
        return self

    def build(self):
        return Book(self.title, self.author, self.isbn)

class BookSearchStrategy:
    """Strategy interface for searching books"""
    def search(self, books, query):
        raise NotImplementedError

class SimpleBookSearchStrategy(BookSearchStrategy):
    """Simple search strategy that searches by title, author, and ISBN"""
    def search(self, books, query):
        results = []
        for book in books:
            if query.lower() in book.title.lower() or query.lower() in book.author.lower() or query.lower() in book.isbn.lower():
                results.append(book)
        return results

class AdvancedBookSearchStrategy(BookSearchStrategy):
    """Sample Advanced Search Strategy"""
    def search(self, books, query, by = ['title, author, ISBN']):
        search_query_words = query.split(" ")
        results = []
        for book in books:
            if all(any(word in getattr(book, field).lower() for field in by) for word in search_query_words):
                results.append(book)
        return results


class BookManager:
    """Manage all books
    """
    def __init__(self) -> None:
        self.books = []
    
    def add_book(self, title, author, isbn):
        """Add a book to the library
        
        Args:
            title (str): Title of the book
            author (str): Author of the book
            isbn (str): ISBN of the book
        """
        try:
            # Check if book exists with same ISBN
            if self._find_book_by_isbn(isbn):
                print("Book with same ISBN already exists.")
                return False

            if not self._isbn_checker(isbn):
                print("ISBN Incorrect")
                return False
            
            # Add the book
            book_builder = BookBuilder().with_title(title).with_author(author).with_isbn(isbn)
            new_book = book_builder.build()
            self.books.append(new_book)
            print("Book added successfully !")

            return True

        except Exception as e:
            print(f"An error occurred while adding the book: {e}")

    def remove_book(self, isbn):
        """Removes a book from the Library

        Args:
            isbn (str): ISBN of book

        Returns:
            bool:
                True if remove operation is successful
                False if book is not found
        """
        try:
            for index, book in enumerate(self.books):
                if book.isbn == isbn:
                    self.books.pop(index)
                    print("Book successfully removed")
                    return True
            print("Requested book not found")
            return False
        
        except Exception as e:
            print(f"An error occurred while removing the book: {e}")
            return False
    
    def get_all_books(self):
        """ 
        Returns:
            list(Book)
        """
        return self.books
    
    def search_book(self, search_query, search_strategy=SimpleBookSearchStrategy()):
        """
        Search for a book
        
        Args:
            search_query (str): Query to search for
            search_strategy (BookSearchStrategy): Strategy for searching books (default: SimpleBookSearchStrategy())

        Returns:
            list(Book): List of found books
        """
        try:
            return search_strategy.search(self.books, search_query)
        except Exception as e:
            print(f"An Exception Occurred : {e}")
            return []

    def _find_book_by_isbn(self, isbn):
        """Internal method to find a book by ISBN
        
        Args:
            isbn (str): ISBN to search for

        Returns:
            Book or None: Book object if found, None otherwise
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def _isbn_checker(self, isbn) -> bool:
        """Internal method to validate ISBN-10 and ISBN-13
        
        Args:
            isbn (str): ISBN to search for

        Returns:
            Book or None: Book object if found, None otherwise
        """
            
        isbn = isbn.replace("-", "").replace(" ", "").upper();
        match = re.search(r'^(\d{9})(\d|X)$', isbn)
        if not match:
            return False

        digits = match.group(1)
        check_digit = 10 if match.group(2) == 'X' else int(match.group(2))

        result = sum((i + 1) * int(digit) for i, digit in enumerate(digits))
        return (result % 11) == check_digit