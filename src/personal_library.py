import sqlite3
from datetime import datetime

class PersonalLibrary:
    def __init__(self, db_name='library.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_tables()

    def create_tables(self):
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
        cursor = self.conn.cursor()
        added_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('INSERT INTO books (title, author, added_date) VALUES (?, ?, ?)', (title, author, added_date))
        self.conn.commit()
        return cursor.lastrowid

    def remove_book(self, book_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        self.conn.commit()

    def add_lender(self, name, address, mobile):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO lendors (name, address, mobile) VALUES (?, ?, ?)', (name, address, mobile))
        self.conn.commit()
        return cursor.lastrowid

    def remove_lender(self, lendor_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM lendors WHERE id = ?', (lendor_id,))
        self.conn.commit()

    def borrow_book(self, lendor_id, book_id):
        cursor = self.conn.cursor()
        # Check if book is already borrowed and not returned
        cursor.execute('SELECT * FROM borrowed WHERE book_id = ? AND returned = 0', (book_id,))
        if cursor.fetchone():
            raise Exception('Book is already borrowed')
        cursor.execute('INSERT INTO borrowed (lendor_id, book_id, returned) VALUES (?, ?, 1)', (lendor_id, book_id))
        self.conn.commit()
        return cursor.lastrowid

    def return_borrowed_book(self, borrowed_id):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE borrowed SET returned = 0 WHERE id = ?', (borrowed_id,))
        self.conn.commit()

    def get_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM books')
        return cursor.fetchall()

    def get_books_borrowed_with_lender_details(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT b.id, b.title, b.author, l.name, l.address, l.mobile, br.id as borrowed_id
                          FROM books b
                          JOIN borrowed br ON b.id = br.book_id
                          JOIN lendors l ON br.lendor_id = l.id
                          WHERE br.returned = 1''')
        return cursor.fetchall()

    def get_books_not_borrowed(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM books WHERE id IN (
            SELECT book_id FROM borrowed WHERE returned = 0
        )''')
        return cursor.fetchall()

    def get_most_borrowed_book(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT b.id, b.title, b.author, COUNT(br.id) as borrow_count
                          FROM books b
                          JOIN borrowed br ON b.id = br.book_id
                          GROUP BY b.id
                          ORDER BY borrow_count DESC
                          LIMIT 1''')
        return cursor.fetchone()

    def get_least_borrowed_book(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT b.id, b.title, b.author, COUNT(br.id) as borrow_count
                          FROM books b
                          LEFT JOIN borrowed br ON b.id = br.book_id
                          GROUP BY b.id
                          ORDER BY borrow_count ASC
                          LIMIT 1''')
        return cursor.fetchone()

    def close(self):
        self.conn.close()
