
"""
test_personal_library.py

Unit tests for PersonalLibrary class. Tests book and lender management, borrowing/returning,
and query methods using a temporary SQLite database.
"""
import unittest
import os
from src.personal_library import PersonalLibrary


class TestPersonalLibrary(unittest.TestCase):
    """
    Unit tests for PersonalLibrary methods.
    Creates a temporary database for each test.
    """

    def test_get_all_lendors(self):
        """
        Test getting all lenders.
        """
        lendor_id1 = self.lib.add_lender('LenderA', 'AddrA', '111')
        lendor_id2 = self.lib.add_lender('LenderB', 'AddrB', '222')
        lendors = self.lib.get_all_lendors()
        self.assertTrue(any(l[0] == lendor_id1 for l in lendors))
        self.assertTrue(any(l[0] == lendor_id2 for l in lendors))
    def setUp(self):
        """
        Set up a fresh test database before each test.
        """
        self.test_db = 'test_library.db'
        # Remove if exists
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.lib = PersonalLibrary(self.test_db)

    def tearDown(self):
        """
        Clean up the test database after each test.
        """
        self.lib.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_and_remove_book(self):
        """
        Test adding and removing a book.
        """
        book_id = self.lib.add_book('Book1', 'Author1')
        books = self.lib.get_all_books()
        self.assertEqual(len(books), 1)
        self.lib.remove_book(book_id)
        books = self.lib.get_all_books()
        self.assertEqual(len(books), 0)

    def test_add_and_remove_lender(self):
        """
        Test adding and removing a lender.
        """
        lendor_id = self.lib.add_lender('Lender1', 'Addr1', '123')
        self.lib.remove_lender(lendor_id)
        # No direct get_lendors, so just check no error

    def test_borrow_and_return_book(self):
        """
        Test borrowing and returning a book.
        """
        book_id = self.lib.add_book('Book2', 'Author2')
        lendor_id = self.lib.add_lender('Lender2', 'Addr2', '456')
        borrowed_id = self.lib.borrow_book(lendor_id, book_id)
        borrowed = self.lib.get_books_borrowed_with_lender_details()
        self.assertEqual(len(borrowed), 1)
        self.lib.return_borrowed_book(borrowed_id)
        borrowed = self.lib.get_books_borrowed_with_lender_details()
        self.assertEqual(len(borrowed), 0)

    def test_get_books_not_borrowed(self):
        """
        Test getting books that are not borrowed.
        """
        book_id = self.lib.add_book('Book3', 'Author3')
        available = self.lib.get_books_not_borrowed()
        self.assertTrue(any(b[0] == book_id for b in available))
        lendor_id = self.lib.add_lender('Lender3', 'Addr3', '789')
        self.lib.borrow_book(lendor_id, book_id)
        available = self.lib.get_books_not_borrowed()
        self.assertFalse(any(b[0] == book_id for b in available))

    def test_most_and_least_borrowed(self):
        """
        Test getting the most and least borrowed books.
        """
        b1 = self.lib.add_book('Book4', 'Author4')
        b2 = self.lib.add_book('Book5', 'Author5')
        l1 = self.lib.add_lender('Lender4', 'Addr4', '111')
        l2 = self.lib.add_lender('Lender5', 'Addr5', '222')
        self.lib.borrow_book(l1, b1)
        self.lib.return_borrowed_book(1)
        self.lib.borrow_book(l2, b1)
        self.lib.return_borrowed_book(2)
        self.lib.borrow_book(l1, b2)
        most = self.lib.get_most_borrowed_book()
        least = self.lib.get_least_borrowed_book()
        self.assertEqual(most[0], b1)
        self.assertEqual(least[0], b2)


if __name__ == '__main__':
    unittest.main()
