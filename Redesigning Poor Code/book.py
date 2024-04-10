# Global list to store books
books = []

def add_book(title, author, isbn):
    books.append({"title": title, "author": author, "isbn": isbn})

def list_books():
    for book in books:
        print(book)

