
"""
personal_library.py

Backend logic for PersonalLibrary Kivy app. Implements book and lender management, borrowing/returning,
and queries for book/lender details using SQLite.
"""
import sqlite3
from datetime import datetime


class PersonalLibrary:
    """
    PersonalLibrary manages books, lenders, and borrowing/returning operations using SQLite.
    """

    def get_book_details(self, book_id):
        """
        Get details of a book by its ID.
        Args:
            book_id (int): ID of the book.
        Returns:
            tuple: Book details (id, title, author, added_date) or None.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        return cursor.fetchone()

    def get_lendor_details(self, lendor_id):
        """
        Get details of a lender by ID.
        Args:
            lendor_id (int): ID of the lender.
        Returns:
            tuple: Lender details (id, name, address, mobile) or None.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM lendors WHERE id = ?', (lendor_id,))
        return cursor.fetchone()

    def get_all_lendors(self):
        """
        Get all lenders in the library.
        Returns:
            list: List of all lenders.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM lendors')
        return cursor.fetchall()

    def __init__(self, db_name='library.db'):
        """
        Initialize the PersonalLibrary with a SQLite database.
        Creates tables if they do not exist.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_tables()

    def create_tables(self):
        """
        Create the books, lendors, and borrowed tables if they do not exist.
        """
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            added_date TEXT NOT NULL
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS lendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            mobile TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS borrowed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lendor_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            returned INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(lendor_id) REFERENCES lendors(id),
            FOREIGN KEY(book_id) REFERENCES books(id)
        )''')
        self.conn.commit()

    def add_book(self, title, author):
        """
        Add a new book to the library.
        Args:
            title (str): Book title.
            author (str): Book author.
        Returns:
            int: ID of the added book.
        """
        cursor = self.conn.cursor()
        added_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute(
            'INSERT INTO books (title, author, added_date) VALUES (?, ?, ?)', (title, author, added_date))
        self.conn.commit()
        return cursor.lastrowid

    def remove_book(self, book_id):
        """
        Remove a book from the library by its ID.
        Args:
            book_id (int): ID of the book to remove.
        """
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        self.conn.commit()

    def add_lender(self, name, address, mobile):
        """
        Add a new lender.
        Args:
            name (str): Lender name.
            address (str): Lender address.
            mobile (str): Lender mobile number.
        Returns:
            int: ID of the added lender.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO lendors (name, address, mobile) VALUES (?, ?, ?)', (name, address, mobile))
        self.conn.commit()
        return cursor.lastrowid

    def remove_lender(self, lendor_id):
        """
        Remove a lender by ID.
        Args:
            lendor_id (int): ID of the lender to remove.
        """
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM lendors WHERE id = ?', (lendor_id,))
        self.conn.commit()

    def borrow_book(self, lendor_id, book_id):
        """
        Borrow a book for a lender.
        Args:
            lendor_id (int): Lender ID.
            book_id (int): Book ID.
        Returns:
            int: ID of the borrowed record.
        Raises:
            Exception: If the book is already borrowed.
        """
        cursor = self.conn.cursor()
        # Check if book is already borrowed and not returned
        cursor.execute('''SELECT id FROM books WHERE id NOT IN (
            SELECT book_id FROM borrowed WHERE returned = 1
        )''')
        if (book_id,) not in cursor.fetchall():
            raise Exception('Book is already borrowed')
        cursor.execute(
            'INSERT INTO borrowed (lendor_id, book_id, returned) VALUES (?, ?, 1)', (lendor_id, book_id))
        self.conn.commit()
        return cursor.lastrowid

    def return_borrowed_book(self, borrowed_id):
        """
        Return a borrowed book by borrowed record ID.
        Args:
            borrowed_id (int): ID of the borrowed record.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE borrowed SET returned = 0 WHERE id = ?', (borrowed_id,))
        self.conn.commit()

    def get_all_books(self):
        """
        Get all books in the library.
        Returns:
            list: List of all books.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM books')
        return cursor.fetchall()

    def get_books_borrowed_with_lender_details(self):
        """
        Get all borrowed books with lender details.
        Returns:
            list: List of borrowed books with lender info.
        """
        cursor = self.conn.cursor()
        cursor.execute('''SELECT b.id, b.title, b.author, l.name, l.address, l.mobile, br.id as borrowed_id
                          FROM books b
                          JOIN borrowed br ON b.id = br.book_id
                          JOIN lendors l ON br.lendor_id = l.id
                          WHERE br.returned = 1''')
        return cursor.fetchall()

    def get_books_not_borrowed(self):
        """
        Get all books that are not currently borrowed.
        Returns:
            list: List of available books.
        """
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM books WHERE id NOT IN (
            SELECT book_id FROM borrowed WHERE returned = 1
        )''')
        return cursor.fetchall()

    def get_most_borrowed_book(self):
        """
        Get the most borrowed book.
        Returns:
            tuple: Book details and borrow count.
        """
        cursor = self.conn.cursor()
        cursor.execute('''SELECT b.id, b.title, b.author, COUNT(br.id) as borrow_count
                          FROM books b
                          JOIN borrowed br ON b.id = br.book_id
                          GROUP BY b.id
                          ORDER BY borrow_count DESC
                          LIMIT 1''')
        return cursor.fetchone()

    def get_least_borrowed_book(self):
        """
        Get the least borrowed book.
        Returns:
            tuple: Book details and borrow count.
        """
        cursor = self.conn.cursor()
        cursor.execute('''SELECT b.id, b.title, b.author, COUNT(br.id) as borrow_count
                          FROM books b
                          LEFT JOIN borrowed br ON b.id = br.book_id
                          GROUP BY b.id
                          ORDER BY borrow_count ASC
                          LIMIT 1''')
        return cursor.fetchone()

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()
