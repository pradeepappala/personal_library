
"""
main.py

Kivy UI for PersonalLibrary management. Provides screens for adding/removing books and lenders,
borrowing/returning books, and viewing book/lender details. Uses src.personal_library.PersonalLibrary
for backend operations.
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from src.personal_library import PersonalLibrary

library = PersonalLibrary()


class MainMenu(Screen):
    """
    Main menu screen with navigation buttons for all PersonalLibrary operations.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        buttons = [
            ("Add Book", "add_book"),
            ("Show All Books", "show_all_books"),
            ("Get Borrowed Books with Lender details", "borrowed_books_lender"),
            ("Show Available Books", "show_available_books"),
            ("Show All Lenders", "show_all_lendors"),
            ("Add Lender", "add_lender"),
            ("Borrow Book", "borrow_book"),
            ("Return Book", "return_book"),
            ("Remove Book", "remove_book"),
            ("Remove Lender", "remove_lender"),
        ]
        for text, screen in buttons:
            btn = Button(text=text)
            btn.bind(on_release=lambda btn, s=screen: setattr(
                self.manager, 'current', s))
            layout.add_widget(btn)
        self.add_widget(layout)


class ShowAllLendorsScreen(Screen):
    """
    Screen to display all lenders in the library.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.result = Label(text='', size_hint_y=None, valign='top', halign='left')
        self.result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.result.text_size = (None, None)
        show_btn = Button(text='Show All Lenders')
        show_btn.bind(on_release=self.show_lendors)
        layout.add_widget(show_btn)
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        scroll.add_widget(self.result)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Back', on_release=lambda x: setattr(
            self.manager, 'current', 'main_menu')))
        self.add_widget(layout)

    def show_lendors(self, instance):
        lendors = library.get_all_lendors()
        self.result.text = '\n\n'.join([
            f"ID: {l[0]}\nName: {l[1]}\nAddress: {l[2]}\nMobile: {l[3]}" for l in lendors
        ])


class AddBookScreen(Screen):
    """
    Screen for adding a new book to the library.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.title_input = TextInput(hint_text='Title')
        self.author_input = TextInput(hint_text='Author')
        add_btn = Button(text='Add Book')
        self.result = Label(text='', size_hint_y=None, valign='top', halign='left')
        self.result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.result.text_size = (None, None)
        add_btn.bind(on_release=self.add_book)
        layout.add_widget(self.title_input)
        layout.add_widget(self.author_input)
        layout.add_widget(add_btn)
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        scroll.add_widget(self.result)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Back', on_release=lambda x: setattr(
            self.manager, 'current', 'main_menu')))
        self.add_widget(layout)

    def add_book(self, instance):
        """Add a book using title and author input fields."""
        title = self.title_input.text.strip()
        author = self.author_input.text.strip()
        if title and author:
            book_id = library.add_book(title, author)
            self.result.text = f"Book added with ID: {book_id}\nTitle: {title}\nAuthor: {author}"
        else:
            self.result.text = "Please enter both title and author."


class RemoveBookScreen(Screen):
    """
    Screen for removing a book by its ID.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.book_id_input = TextInput(hint_text='Book ID')
        remove_btn = Button(text='Remove Book')
        show_book_btn = Button(text='Show Book Details')
        self.result = Label(text='', size_hint_y=None, valign='top', halign='left')
        self.result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.result.text_size = (None, None)
        remove_btn.bind(on_release=self.remove_book)
        show_book_btn.bind(on_release=self.show_book_details)
        layout.add_widget(self.book_id_input)
        layout.add_widget(show_book_btn)
        layout.add_widget(remove_btn)
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        scroll.add_widget(self.result)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Back', on_release=lambda x: setattr(
            self.manager, 'current', 'main_menu')))
        self.add_widget(layout)

    def show_book_details(self, instance):
        try:
            book_id = int(self.book_id_input.text.strip())
            b = library.get_book_details(book_id)
            if b:
                self.result.text = f"Book Details:\nID: {b[0]}\nTitle: {b[1]}\nAuthor: {b[2]}\nAdded: {b[3]}"
            else:
                self.result.text = "Book not found."
        except Exception as e:
            self.result.text = str(e)

    def remove_book(self, instance):
        """Remove a book using the provided book ID."""
        try:
            book_id = int(self.book_id_input.text.strip())
            library.remove_book(book_id)
            self.result.text = f"Book removed.\nID: {book_id}"
        except Exception as e:
            self.result.text = str(e)


class ShowAllBooksScreen(Screen):
    """
    Screen to display all books in the library.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.result = Label(text='', size_hint_y=None, valign='top', halign='left')
        self.result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.result.text_size = (None, None)
        show_btn = Button(text='Show All Books')
        show_btn.bind(on_release=self.show_books)
        layout.add_widget(show_btn)
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        scroll.add_widget(self.result)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Back', on_release=lambda x: setattr(
            self.manager, 'current', 'main_menu')))
        self.add_widget(layout)

    def show_books(self, instance):
        """Show all books in the library."""
        books = library.get_all_books()
        self.result.text = '\n\n'.join(
            [f"ID: {b[0]}\nTitle: {b[1]}\nAuthor: {b[2]}" for b in books])


class ShowAvailableBooksScreen(Screen):
    """
    Screen to display all available (not borrowed) books.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.result = Label(text='', size_hint_y=None, valign='top', halign='left')
        self.result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.result.text_size = (None, None)
        show_btn = Button(text='Show Available Books')
        show_btn.bind(on_release=self.show_books)
        layout.add_widget(show_btn)
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        scroll.add_widget(self.result)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Back', on_release=lambda x: setattr(
            self.manager, 'current', 'main_menu')))
        self.add_widget(layout)

    def show_books(self, instance):
        """Show all available books."""
        books = library.get_books_not_borrowed()
        self.result.text = '\n\n'.join(
            [f"ID: {b[0]}\nTitle: {b[1]}\nAuthor: {b[2]}" for b in books])


class AddLenderScreen(Screen):
    """
    Screen for adding a new lender.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.name_input = TextInput(hint_text='Name')
        self.address_input = TextInput(hint_text='Address')
        self.mobile_input = TextInput(hint_text='Mobile')
        add_btn = Button(text='Add Lender')
        self.result = Label(text='', size_hint_y=None, valign='top', halign='left')
        self.result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.result.text_size = (None, None)
        add_btn.bind(on_release=self.add_lender)
        layout.add_widget(self.name_input)
        layout.add_widget(self.address_input)
        layout.add_widget(self.mobile_input)
        layout.add_widget(add_btn)
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        scroll.add_widget(self.result)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Back', on_release=lambda x: setattr(
            self.manager, 'current', 'main_menu')))
        self.add_widget(layout)

    def add_lender(self, instance):
        """Add a lender using name, address, and mobile input fields."""
        name = self.name_input.text.strip()
        address = self.address_input.text.strip()
        mobile = self.mobile_input.text.strip()
        if name:
            lendor_id = library.add_lender(name, address, mobile)
            self.result.text = f"Lender added with ID: {lendor_id}\nName: {name}\nAddress: {address}\nMobile: {mobile}"
        else:
            self.result.text = "Please enter lender name."


class RemoveLenderScreen(Screen):
    """
    Screen for removing a lender by ID.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.lender_id_input = TextInput(hint_text='Lender ID')
        remove_btn = Button(text='Remove Lender')
        show_lender_btn = Button(text='Show Lender Details')
        self.result = Label(text='', size_hint_y=None, valign='top', halign='left')
        self.result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.result.text_size = (None, None)
        show_lender_btn.bind(on_release=self.show_lender_details)
        remove_btn.bind(on_release=self.remove_lender)
        layout.add_widget(self.lender_id_input)
        layout.add_widget(show_lender_btn)
        layout.add_widget(remove_btn)
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        scroll.add_widget(self.result)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Back', on_release=lambda x: setattr(
            self.manager, 'current', 'main_menu')))
        self.add_widget(layout)

    def show_lender_details(self, instance):
        try:
            lendor_id = int(self.lender_id_input.text.strip())
            l = library.get_lendor_details(lendor_id)
            if l:
                self.result.text = f"Lender Details:\nID: {l[0]}\nName: {l[1]}\nAddress: {l[2]}\nMobile: {l[3]}"
            else:
                self.result.text = "Lender not found."
        except Exception as e:
            self.result.text = str(e)

    def remove_lender(self, instance):
        """Remove a lender using the provided lender ID."""
        try:
            lendor_id = int(self.lender_id_input.text.strip())
            library.remove_lender(lendor_id)
            self.result.text = f"Lender removed.\nID: {lendor_id}"
        except Exception as e:
            self.result.text = str(e)


class BorrowBookScreen(Screen):
    """
    Screen for borrowing a book by specifying lender and book IDs.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.lender_id_input = TextInput(hint_text='Lender ID')
        self.book_id_input = TextInput(hint_text='Book ID')
        borrow_btn = Button(text='Borrow Book')
        show_lender_btn = Button(text='Show Lender Details')
        show_book_btn = Button(text='Show Book Details')
        self.result = Label(text='', size_hint_y=None, valign='top', halign='left')
        self.result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.result.text_size = (None, None)
        borrow_btn.bind(on_release=self.borrow_book)
        show_lender_btn.bind(on_release=self.show_lender_details)
        show_book_btn.bind(on_release=self.show_book_details)
        layout.add_widget(self.lender_id_input)
        layout.add_widget(show_lender_btn)
        layout.add_widget(self.book_id_input)
        layout.add_widget(show_book_btn)
        layout.add_widget(borrow_btn)
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        scroll.add_widget(self.result)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Back', on_release=lambda x: setattr(
            self.manager, 'current', 'main_menu')))
        self.add_widget(layout)

    def show_lender_details(self, instance):
        try:
            lendor_id = int(self.lender_id_input.text.strip())
            l = library.get_lendor_details(lendor_id)
            if l:
                self.result.text = f"Lender Details:\nID: {l[0]}\nName: {l[1]}\nAddress: {l[2]}\nMobile: {l[3]}"
            else:
                self.result.text = "Lender not found."
        except Exception as e:
            self.result.text = str(e)

    def show_book_details(self, instance):
        try:
            book_id = int(self.book_id_input.text.strip())
            b = library.get_book_details(book_id)
            if b:
                self.result.text = f"Book Details:\nID: {b[0]}\nTitle: {b[1]}\nAuthor: {b[2]}\nAdded: {b[3]}"
            else:
                self.result.text = "Book not found."
        except Exception as e:
            self.result.text = str(e)

    def borrow_book(self, instance):
        """Borrow a book using lender and book IDs."""
        try:
            lendor_id = int(self.lender_id_input.text.strip())
            book_id = int(self.book_id_input.text.strip())
            borrowed_id = library.borrow_book(lendor_id, book_id)
            self.result.text = f"Book borrowed.\nBook ID: {book_id}\nLender ID: {lendor_id}\nBorrowed ID: {borrowed_id}"
        except Exception as e:
            self.result.text = str(e)


class ReturnBookScreen(Screen):
    """
    Screen for returning a borrowed book by borrowed ID.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.borrowed_id_input = TextInput(hint_text='Borrowed ID')
        return_btn = Button(text='Return Book')
        show_lender_btn = Button(text='Show Lender Details')
        show_book_btn = Button(text='Show Book Details')
        self.result = Label(text='', size_hint_y=None, valign='top', halign='left')
        self.result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.result.text_size = (None, None)
        return_btn.bind(on_release=self.return_book)
        show_lender_btn.bind(on_release=self.show_lender_details)
        show_book_btn.bind(on_release=self.show_book_details)
        layout.add_widget(self.borrowed_id_input)
        layout.add_widget(show_lender_btn)
        layout.add_widget(show_book_btn)
        layout.add_widget(return_btn)
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        scroll.add_widget(self.result)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Back', on_release=lambda x: setattr(
            self.manager, 'current', 'main_menu')))
        self.add_widget(layout)

    def show_lender_details(self, instance):
        try:
            borrowed_id = int(self.borrowed_id_input.text.strip())
            cursor = library.conn.cursor()
            cursor.execute('SELECT lendor_id, book_id FROM borrowed WHERE id = ?', (borrowed_id,))
            row = cursor.fetchone()
            if row:
                lendor_id, book_id = row
                l = library.get_lendor_details(lendor_id)
                if l:
                    self.result.text = f"Lender Details:\nID: {l[0]}\nName: {l[1]}\nAddress: {l[2]}\nMobile: {l[3]}"
                else:
                    self.result.text = "Lender not found."
            else:
                self.result.text = "Borrowed record not found."
        except Exception as e:
            self.result.text = str(e)

    def show_book_details(self, instance):
        try:
            borrowed_id = int(self.borrowed_id_input.text.strip())
            cursor = library.conn.cursor()
            cursor.execute('SELECT lendor_id, book_id FROM borrowed WHERE id = ?', (borrowed_id,))
            row = cursor.fetchone()
            if row:
                lendor_id, book_id = row
                b = library.get_book_details(book_id)
                if b:
                    self.result.text = f"Book Details:\nID: {b[0]}\nTitle: {b[1]}\nAuthor: {b[2]}\nAdded: {b[3]}"
                else:
                    self.result.text = "Book not found."
            else:
                self.result.text = "Borrowed record not found."
        except Exception as e:
            self.result.text = str(e)

    def return_book(self, instance):
        """Return a borrowed book using borrowed ID."""
        try:
            borrowed_id = int(self.borrowed_id_input.text.strip())
            library.return_borrowed_book(borrowed_id)
            self.result.text = f"Book returned.\nBorrowed ID: {borrowed_id}"
        except Exception as e:
            self.result.text = str(e)


class BorrowedBooksLenderScreen(Screen):
    """
    Screen to show borrowed books with lender details.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        show_btn = Button(text='Show Borrowed Books with Lender Details')
        show_btn.bind(on_release=self.show_borrowed)
        layout.add_widget(show_btn)
        # Create a scrollable label for results
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        self.result = Label(text='', size_hint_y=None, valign='top', halign='left')
        self.result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.result.text_size = (None, None)
        scroll.add_widget(self.result)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Back', on_release=lambda x: setattr(
            self.manager, 'current', 'main_menu')))
        self.add_widget(layout)

    def show_borrowed(self, instance):
        """Show borrowed books with lender details."""
        books = library.get_books_borrowed_with_lender_details()
        self.result.text = '\n\n'.join(
            [f"Book ID: {b[0]}\nTitle: {b[1]}\nAuthor: {b[2]}\nLender: {b[3]}\nAddress: {b[4]}\nMobile: {b[5]}\nBorrowed ID: {b[6]}" for b in books])


class PersonalLibraryApp(App):
    """
    Main Kivy App class. Sets up the ScreenManager and all screens.
    """

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(AddBookScreen(name='add_book'))
        sm.add_widget(ShowAllBooksScreen(name='show_all_books'))
        sm.add_widget(BorrowedBooksLenderScreen(name='borrowed_books_lender'))
        sm.add_widget(ShowAvailableBooksScreen(name='show_available_books'))
        sm.add_widget(ShowAllLendorsScreen(name='show_all_lendors'))
        sm.add_widget(AddLenderScreen(name='add_lender'))
        sm.add_widget(BorrowBookScreen(name='borrow_book'))
        sm.add_widget(ReturnBookScreen(name='return_book'))
        sm.add_widget(RemoveBookScreen(name='remove_book'))
        sm.add_widget(RemoveLenderScreen(name='remove_lender'))
        return sm


if __name__ == '__main__':
    run_ui = True
    if run_ui:
        PersonalLibraryApp().run()
    else:
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
