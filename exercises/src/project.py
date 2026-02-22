"""
Exercise 4: Mini-Project - Library Management System
=====================================================
Combine everything: functions, classes, files, and JSON

This exercise brings together all the concepts from the course.
Build a simple library system that tracks books and borrowers.

Instructions:
- Complete all TODOs
- The system should persist data to JSON files
- Run this file to test your implementation

Run with: python exercise_4_project.py
"""

import json
import os
from datetime import datetime
from os import name
from traceback import format_tb

from coverage.files import actual_path


# =============================================================================
# PART 1: HELPER FUNCTIONS
# =============================================================================

def format_date(dt: datetime = None) -> str:
    """
    Format a datetime object as a string "YYYY-MM-DD".
    If no datetime provided, use current date.

    Example:
        format_date(datetime(2024, 1, 15)) -> "2024-01-15"
        format_date() -> "2024-02-04" (today's date)
    """
    # TODO: Implement this function
    if dt is None:
        dt=datetime.today()
    return dt.strftime("%Y-%m-%d")



def generate_id(prefix: str, existing_ids: list) -> str:
    next_num = len(existing_ids) + 1
    return f"{prefix}_{next_num:04d}"


"""
    Generate a new unique ID with the given prefix.

    Parameters:
        prefix: String prefix (e.g., "BOOK", "USER")
        existing_ids: List of existing IDs to avoid duplicates

    Returns:
        New ID in format "{prefix}_{number:04d}"

    Example:
        generate_id("BOOK", ["BOOK_0001", "BOOK_0002"]) -> "BOOK_0003"
        generate_id("USER", []) -> "USER_0001"
    """
    # TODO: Implement this function
    # Hint: Find the highest existing number and add 1


# use contains and redo this one
def search_items(items: list, **criteria) -> list:
    results=[]
    for item in items:
        match=True
        for key, expected in criteria.items():
            actual=item.get(key)
            if isinstance(actual, str) and isinstance(expected, str):
                if actual.lower() != expected.lower():
                  match = False
                  break
            else:
                if actual != expected:
                    match = False
                    break
            if match:
                    results.append(item)

    return results
"""
    Search a list of dictionaries by matching criteria.
    Uses **kwargs to accept any search fields.

    Parameters:
        items: List of dictionaries to search
        **criteria: Field-value pairs to match (case-insensitive for strings)

    Returns:
        List of matching items

    Example:
        books = [
            {"title": "Python 101", "author": "Smith"},
            {"title": "Java Guide", "author": "Smith"},
            {"title": "Python Advanced", "author": "Jones"}
        ]
        search_items(books, author="Smith") -> [first two books]
        search_items(books, title="Python 101") -> [first book]
    """
    # TODO: Implement this function
    # Hint: For each item, check if ALL criteria match




# =============================================================================
# PART 2: BOOK CLASS
# =============================================================================

class Book:
    """
    Represents a book in the library.

    Class Attributes:
        GENRES: List of valid genres ["Fiction", "Non-Fiction", "Science", "History", "Technology"]

    Instance Attributes:
        book_id (str): Unique identifier
        title (str): Book title
        author (str): Author name
        genre (str): Must be one of GENRES
        available (bool): Whether book is available for borrowing

    Methods:
        to_dict(): Convert to dictionary for JSON serialization
        from_dict(data): Class method to create Book from dictionary
        __str__(): Return readable string representation
    """

    GENRES = ["Fiction", "Non-Fiction", "Science", "History", "Technology"]

    def __init__(self, book_id: str, title: str, author: str, genre: str, available: bool = True):
        # TODO: Initialize attributes
        # TODO: Validate that genre is in GENRES, raise ValueError if not
        self.book_id=book_id
        self.title=title
        self.author=author
        self.available=available
        self.genre=genre
        if not genre in self.GENRES:
          raise ValueError("Not a genre")



    def to_dict(self) -> dict:
        # TODO: Return dictionary with all attributes
        books={"book_id":self.book_id, "title": self.title, "author": self.author, "genre": self.genre, "available":self.available}
        return books

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        # TODO: Create and return a Book instance from dictionary
        data.get("book_id")
        data.get("title")
        data.get("author")
        data.get("genre")
        data.get("available", True)
        b=Book(data.get("book_id"),data.get("title"),data.get("author"),data.get("available"), data.get("genre") )
        return b

    def __str__(self) -> str:
        # TODO: Return string like "[BOOK_0001] Python 101 by Smith (Technology) - Available"
        return f'{self.book_id} {self.title} by {self.author}({self.genre}) -{self.available}'


# =============================================================================
# PART 3: BORROWER CLASS
# =============================================================================

class Borrower:
    """
    Represents a library member who can borrow books.

    Instance Attributes:
        borrower_id (str): Unique identifier
        name (str): Borrower's name
        email (str): Borrower's email
        borrowed_books (list): List of book_ids currently borrowed

    Methods:
        borrow_book(book_id): Add book to borrowed list
        return_book(book_id): Remove book from borrowed list
        to_dict(): Convert to dictionary
        from_dict(data): Class method to create Borrower from dictionary
    """

    MAX_BOOKS = 3  # Maximum books a borrower can have at once

    def __init__(self, borrower_id: str, name: str, email: str, borrowed_books: list = None):
        # TODO: Initialize attributes (use empty list if borrowed_books is None)
        self.borrower_id=borrower_id
        self.name=name
        self.email=email
        self.borrowed_books=borrowed_books or []


    def can_borrow(self) -> bool:
        """Check if borrower can borrow more books."""
        # TODO: Return True if len(borrowed_books) < MAX_BOOKS
        if len(self.borrowed_books) < self.MAX_BOOKS:
            return True
        else:
            return False


    def borrow_book(self, book_id: str) -> bool:
        """Add book to borrowed list. Return False if at max limit."""
        # TODO: Implement this method
        if self.can_borrow():
            self.borrowed_books.append(book_id)
            return True
        else:
            return False

    def return_book(self, book_id: str) -> bool:
        """Remove book from borrowed list. Return False if not found."""
        # TODO: Implement this method
        if book_id in  self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        else:
            return False

    def to_dict(self) -> dict:
        # TODO: Return dictionary with all attributes
        return {"borrower_id": self.borrower_id, "name":self.name, "email": self.email, "borrowed_books":self.borrowed_books}

    @classmethod
    def from_dict(cls, data: dict) -> "Borrower":
        # TODO: Create and return a Borrower instance from dictionary
        borrower=Borrower(data.get("borrower_id"),data.get("name"),data.get("email"), data.get("borrowed_books"))
        return borrower

# =============================================================================
# PART 4: LIBRARY CLASS (Main System)
# =============================================================================

class Library:
    """
    Main library system that manages books and borrowers.
    Persists data to JSON files.

    Attributes:
        name (str): Library name
        books (dict): book_id -> Book
        borrowers (dict): borrower_id -> Borrower
        books_file (str): Path to books JSON file
        borrowers_file (str): Path to borrowers JSON file

    Methods:
        add_book(title, author, genre) -> Book: Add a new book
        add_borrower(name, email) -> Borrower: Add a new borrower
        checkout_book(book_id, borrower_id) -> bool: Borrower checks out a book
        return_book(book_id, borrower_id) -> bool: Borrower returns a book
        search_books(**criteria) -> list: Search books by criteria
        get_available_books() -> list: Get all available books
        get_borrower_books(borrower_id) -> list: Get books borrowed by a borrower
        save(): Save all data to JSON files
        load(): Load data from JSON files
    """

    def __init__(self, name: str, data_dir: str = "."):
        self.name = name
        self.books = {}
        self.borrowers = {}
        self.books_file = os.path.join(data_dir, "library_books.json")
        self.borrowers_file = os.path.join(data_dir, "library_borrowers.json")
        self.load()
        # TODO: Call self.load() to load existing data

    def load(self) -> None:
        """Load books and borrowers from JSON files."""
        # TODO: Load books from self.books_file
        # TODO: Load borrowers from self.borrowers_file
        # Hint: Use try/except to handle files not existing
        try:
            with open(self.books_file, "r", encoding="utf-8") as f:
                book_list=json.load(f)
                self.books={b["book_id"]: Book.from_dict(b) for b in book_list}
        except:
            self.books = {}  # initialize empty dict if file not found
        try:
                with open(self.borrowers_file, "r", encoding="utf-8") as h:
                 borrowers_list=json.load(h)
                 self.borrowers={b["borrower_id"]: Borrower.from_dict(b) for b in borrowers_list}
        except:
            self.borrowers = {}

    def save(self) -> None:
        """Save books and borrowers to JSON files."""
        # TODO: Save self.books to self.books_file
        # TODO: Save self.borrowers to self.borrowers_file
        books_data = [book.to_dict() for book in self.books]
        borrow_data=[borrower.to_dict() for borrower in self.borrowers]
        # Hint: Convert Book/Borrower objects to dicts using to_dict()
        with open(self.books_file, "w", encoding="utf-8") as f:
            json.dump(books_data, f, indent=2)
        with open(self.borrowers_file, "w", encoding="utf-8") as f:
            json.dump(borrow_data, f, indent=2)

    def add_book(self, title: str, author: str, genre: str) -> Book:
        """Add a new book to the library."""
        # TODO: Generate new book_id using generate_id
        # TODO: Create Book, add to self.books, save, and return
        new_id=generate_id(title,self.books.get("book_id"))
        b=Book(new_id,title,author,genre,True)
        return b

    def add_borrower(self, name: str, email: str) -> Borrower:
        """Register a new borrower."""
        # TODO: Generate new borrower_id, create Borrower, add to self.borrowers, save, return
        borrower_list=[]
        for borrower in self.borrowers:
          borrower_list.append(borrower)

        new_id=generate_id("User",borrower_list)
        borrower=Borrower(new_id,name,email)
        self.borrowers[new_id]=borrower
        self.save()
        return borrower

    def checkout_book(self, book_id: str, borrower_id: str) -> bool:
        """
        Borrower checks out a book.
        Returns False if book unavailable, borrower not found, or at max limit.
        """
        # TODO: Validate book exists and is available
        # TODO: Validate borrower exists and can borrow
        # TODO: Update book.available, borrower.borrowed_books
        # TODO: Save and return True
        book=self.books.get(book_id)
        if book is None:
            return False
        if not book.available:
            return False
        borrower=self.borrowers.get(borrower_id)
        if borrower is None:
            return False
        if not borrower.can_borrow():
            return False
        book.available=False
        borrower.borrowed_books(book_id)
        self.save()
        return True


    def return_book(self, book_id: str, borrower_id: str) -> bool:
        """
        Borrower returns a book.
        Returns False if book/borrower not found or book wasn't borrowed by this person.
        """
        # TODO: Validate book and borrower exist
        # TODO: Validate book is in borrower's borrowed_books
        # TODO: Update book.available, remove from borrowed_books
        # TODO: Save and return True
        book=self.books.get(book_id)
        borrower=self.borrowers.get(borrower_id)
        if book or borrower is None:
            return False
        if borrower.borrowed_books(book_id):
            book.available=True
        self.save()
        return True

    def search_books(self, **criteria) -> list:
        """Search books by any criteria (title, author, genre, available)."""
        # TODO: Use search_items helper function
        # Hint: Convert self.books.values() to list of dicts first
        book_dicts = [b.to_dict() for b in self.books.values()]
        matched_dicts = search_items(book_dicts, **criteria)
        result_books = [self.books[d["book_id"]] for d in matched_dicts]
        return result_books


    def get_available_books(self) -> list:
        """Get list of all available books."""
        avail_list=[]
        for book in self.books:
            if book.available:
                avail_list.append(book)
        return avail_list


    def get_borrower_books(self, borrower_id: str) -> list:
        """Get list of books currently borrowed by a borrower."""
        # TODO: Get borrower, return list of Book objects for their borrowed_books
        borrower=self.borrowers.get(borrower_id)
        if borrower is None:
            return []
        else:
            #review again. this one was hard
            return [self.books[bk_id] for bk_id in borrower.borrowed_books if bk_id in self.books]


    def get_statistics(self) -> dict:
        """
        Return library statistics.
        Uses the concepts of dict comprehension and aggregation.
        """
        # TODO: Return dict with:
        # - total_books: total number of books
        # - available_books: number of available books
        # - checked_out: number of checked out books
        # - total_borrowers: number of borrowers
        # - books_by_genre: dict of genre -> count
        books=list(self.books.values())
        total_books=len(books)
        available_books=sum(1 for b in books if b.available)
        checked_out=total_books-available_books
        total_borrowers=len(self.borrowers)
        books_by_g={}
        for b in books:
            books_by_g[b.genre] = books_by_g.get(b.genre, 0) + 1
        return {
                "total_books": total_books,
                "available_books": available_books,
                "checked_out": checked_out,
                "total_borrowers": total_borrowers,
                "books_by_genre": books_by_g,
            }


