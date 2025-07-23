from src.personal_library import PersonalLibrary

if __name__ == '__main__':
    lib = PersonalLibrary()
    # Add books
    b1 = lib.add_book('The Hobbit', 'J.R.R. Tolkien')
    b2 = lib.add_book('1984', 'George Orwell')
    # Add lenders
    l1 = lib.add_lender('Alice', '123 Main St', '555-1234')
    l2 = lib.add_lender('Bob', '456 Elm St', '555-5678')
    # Borrow a book
    borrow_id1 = lib.borrow_book(l1, b1)
    print('Books borrowed:')
    for row in lib.get_books_borrowed_with_lender_details():
        print(row)

    borrow_id2 = lib.borrow_book(l2, b2)
    print('Books borrowed:')
    for row in lib.get_books_borrowed_with_lender_details():
        print(row)

    print('Books available:')
    for row in lib.get_books_not_borrowed():
        print(row)
    # Return the book
    lib.return_borrowed_book(borrow_id1)
    print('Books available:')
    for row in lib.get_books_not_borrowed():
        print(row)
    print(borrow_id1, borrow_id2)
    lib.return_borrowed_book(borrow_id2)
    print('Books available:')
    for row in lib.get_books_not_borrowed():
        print(row)

    # Most/least borrowed
    print('Most borrowed:', lib.get_most_borrowed_book())
    print('Least borrowed:', lib.get_least_borrowed_book())
    lib.close()
