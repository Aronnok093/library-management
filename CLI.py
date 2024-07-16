import json

class Book:
    def __init__(self, title, authors, isbn, publishing_year, price, quantity):
        self.title = title
        self.authors = authors
        self.isbn = isbn
        self.publishing_year = publishing_year
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.title} by {', '.join(self.authors)} (ISBN: {self.isbn}, Year: {self.publishing_year}, Price: {self.price}, Quantity: {self.quantity})"


class BookCollection:
    def __init__(self):
        self.books = {}
        self.lent_books = {}

    def add_book(self, book):
        if book.isbn in self.books:
            self.books[book.isbn].quantity += book.quantity
        else:
            self.books[book.isbn] = book
        self.save_to_file('books.json')

    def remove_book(self, search_term):
        book = self.search_books(search_term)
        if book:
            del self.books[book.isbn]
            self.save_to_file('books.json')
            return f"Book '{book.title}' removed."
        else:
            return "This book isn’t available to remove."

    def search_books(self, search_term):
        for book in self.books.values():
            if search_term in book.title or search_term in book.isbn:
                return book
        return None

    def search_books_by_author(self, author_name):
        result = []
        for book in self.books.values():
            if any(author_name in author for author in book.authors):
                result.append(book)
        return result

    def lend_book(self, isbn, borrower):
        if isbn in self.books and self.books[isbn].quantity > 0:
            self.books[isbn].quantity -= 1
            if isbn in self.lent_books:
                self.lent_books[isbn].append((borrower, 1))
            else:
                self.lent_books[isbn] = [(borrower, 1)]
            self.save_to_file('books.json')
            return f"Book '{self.books[isbn].title}' lent to {borrower}."
        else:
            return "Not enough books available to lend."

    def return_book(self, isbn, borrower):
        if isbn in self.lent_books:
            for i, (b, qty) in enumerate(self.lent_books[isbn]):
                if b == borrower:
                    self.books[isbn].quantity += 1
                    self.lent_books[isbn].pop(i)
                    if not self.lent_books[isbn]:
                        del self.lent_books[isbn]
                    self.save_to_file('books.json')
                    return f"Book '{self.books[isbn].title}' returned by {borrower}."
        return "This book wasn't lent."

    def save_to_file(self, file_path):
        data = {
            'books': {isbn: vars(book) for isbn, book in self.books.items()},
            'lent_books': self.lent_books
        }
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.books = {isbn: Book(**book) for isbn, book in data['books'].items()}
                self.lent_books = data['lent_books']
        except FileNotFoundError:
            pass


class UserInterface:
    def __init__(self, book_collection):
        self.book_collection = book_collection

    def display_books(self):
        for book in self.book_collection.books.values():
            print(book)

    def search_books(self, search_term):
        book = self.book_collection.search_books(search_term)
        if book:
            print(book)
        else:
            print("No books found.")

    def search_books_by_author(self, author_name):
        books = self.book_collection.search_books_by_author(author_name)
        if books:
            for book in books:
                print(book)
        else:
            print("No books found.")

    def lend_book(self, isbn, borrower):
        result = self.book_collection.lend_book(isbn, borrower)
        print(result)

    def return_book(self, isbn, borrower):
        result = self.book_collection.return_book(isbn, borrower)
        print(result)

    def add_book(self):
        title = input("Enter title: ")
        authors = input("Enter authors (comma separated): ").split(',')
        isbn = input("Enter ISBN: ")
        publishing_year = int(input("Enter publishing year: "))
        price = float(input("Enter price: "))
        quantity = int(input("Enter quantity: "))
        book = Book(title, authors, isbn, publishing_year, price, quantity)
        self.book_collection.add_book(book)

    def remove_book(self, search_term):
        result = self.book_collection.remove_book(search_term)
        print(result)


def main():
    book_collection = BookCollection()
    book_collection.load_from_file('books.json')
    ui = UserInterface(book_collection)

    while True:
        print("\n1. Add Book\n2. Remove Book\n3. Search Book\n4. Search by Author\n5. Lend Book\n6. Return Book\n7. Display Books\n8. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            ui.add_book()
        elif choice == '2':
            term = input("Enter title or ISBN to remove: ")
            ui.remove_book(term)
        elif choice == '3':
            term = input("Enter title or ISBN to search: ")
            ui.search_books(term)
        elif choice == '4':
            author = input("Enter author name to search: ")
            ui.search_books_by_author(author)
        elif choice == '5':
            isbn = input("Enter ISBN to lend: ")
            borrower = input("Enter borrower name: ")
            ui.lend_book(isbn, borrower)
        elif choice == '6':
            isbn = input("Enter ISBN to return: ")
            borrower = input("Enter borrower name: ")
            ui.return_book(isbn, borrower)
        elif choice == '7':
            ui.display_books()
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
