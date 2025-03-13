import sqlite3
import sys
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.conn.commit()

    def create_tables(self):
        """Create the necessary tables if they don't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT,
                category TEXT,
                status TEXT DEFAULT 'To Read',
                added_date TEXT,
                notes TEXT
            )
        ''')
        self.conn.commit()

    def add_book(self, title, author, isbn="", category="", status="To Read", notes=""):
        added_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO books (title, author, isbn, category, status, added_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, author, isbn, category, status, added_date, notes))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_books(self):
        self.cursor.execute('SELECT * FROM books ORDER BY title')
        return self.cursor.fetchall()

    def search_books(self, query):
        search_query = f"%{query}%"
        self.cursor.execute('''
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
            ORDER BY title
        ''', (search_query, search_query, search_query))
        return self.cursor.fetchall()

    def update_book(self, book_id, title, author, isbn, category, status, notes):
        self.cursor.execute('''
            UPDATE books 
            SET title=?, author=?, isbn=?, category=?, status=?, notes=?
            WHERE id=?
        ''', (title, author, isbn, category, status, notes, book_id))
        self.conn.commit()

    def delete_book(self, book_id):
        self.cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
        self.conn.commit()

    def get_book_by_id(self, book_id):
        self.cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
        return self.cursor.fetchone()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


def add_book_from_cli():
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()
    isbn = input("Enter ISBN (optional): ").strip()
    category = input("Enter Category (optional): ").strip()
    status = input("Enter Status (Default: To Read): ").strip() or "To Read"
    notes = input("Enter Notes (optional): ").strip()

    db = DatabaseManager()
    book_id = db.add_book(title, author, isbn, category, status, notes)
    print(f"\n✅ Book added successfully! Book ID: {book_id}")


def search_books_from_cli():
    query = input("Enter search query (title, author, or ISBN): ").strip()
    db = DatabaseManager()
    results = db.search_books(query)
    if results:
        for book in results:
            print(book)
    else:
        print("❌ No books found.")


def update_book_from_cli():
    book_id = input("Enter Book ID to update: ").strip()
    db = DatabaseManager()
    book = db.get_book_by_id(book_id)
    if not book:
        print("❌ Book not found.")
        return

    title = input(f"Enter new title [{book[1]}]: ").strip() or book[1]
    author = input(f"Enter new author [{book[2]}]: ").strip() or book[2]
    isbn = input(f"Enter new ISBN [{book[3]}]: ").strip() or book[3]
    category = input(f"Enter new category [{book[4]}]: ").strip() or book[4]
    status = input(f"Enter new status [{book[5]}]: ").strip() or book[5]
    notes = input(f"Enter new notes [{book[7]}]: ").strip() or book[7]

    db.update_book(book_id, title, author, isbn, category, status, notes)
    print("✅ Book updated successfully!")


def delete_book_from_cli():
    book_id = input("Enter Book ID to delete: ").strip()
    db = DatabaseManager()
    db.delete_book(book_id)
    print("✅ Book deleted successfully!")


def list_books():
    db = DatabaseManager()
    books = db.get_all_books()
    for book in books:
        print(book)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "add_book":
            add_book_from_cli()
        elif command == "search":
            search_books_from_cli()
        elif command == "update_book":
            update_book_from_cli()
        elif command == "delete_book":
            delete_book_from_cli()
        elif command == "list_books":
            list_books()
        else:
            print("❌ Invalid command. Use: add_book, search, update_book, delete_book, or list_books")
    else:
        print("Usage: python database.py <command>")
