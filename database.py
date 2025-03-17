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
                publication_year INTEGER,
                genre TEXT,
                read_status BOOLEAN DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_book(self, title, author, publication_year, genre, read_status=False):
        self.cursor.execute('''
            INSERT INTO books (title, author, publication_year, genre, read_status)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, author, publication_year, genre, read_status))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_books(self):
        self.cursor.execute('SELECT * FROM books ORDER BY title')
        return self.cursor.fetchall()

    def search_books(self, query):
        search_query = f"%{query}%"
        self.cursor.execute('''
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?
            ORDER BY title
        ''', (search_query, search_query, search_query))
        return self.cursor.fetchall()

    def update_book(self, book_id, title, author, publication_year, genre, read_status):
        self.cursor.execute('''
            UPDATE books 
            SET title=?, author=?, publication_year=?, genre=?, read_status=?
            WHERE id=?
        ''', (title, author, publication_year, genre, read_status, book_id))
        self.conn.commit()

    def delete_book(self, book_id):
        self.cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
        self.conn.commit()

    def get_book_by_id(self, book_id):
        self.cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
        return self.cursor.fetchone()
    
    def get_statistics(self):
        self.cursor.execute('SELECT COUNT(*) FROM books')
        total_books = self.cursor.fetchone()[0]
        self.cursor.execute('SELECT COUNT(*) FROM books WHERE read_status=1')
        read_books = self.cursor.fetchone()[0]
        read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
        return total_books, read_books, read_percentage

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

def add_book_from_cli():
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()
    publication_year = input("Enter Publication Year: ").strip()
    genre = input("Enter Genre: ").strip()
    read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

    db = DatabaseManager()
    book_id = db.add_book(title, author, publication_year, genre, read_status)
    print(f"\n✅ Book added successfully! Book ID: {book_id}")

def search_books_from_cli():
    query = input("Enter search query (title, author, or genre): ").strip()
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
    publication_year = input(f"Enter new publication year [{book[3]}]: ").strip() or book[3]
    genre = input(f"Enter new genre [{book[4]}]: ").strip() or book[4]
    read_status = input(f"Have you read this book? (yes/no) [{book[5]}]: ").strip().lower() == "yes"

    db.update_book(book_id, title, author, publication_year, genre, read_status)
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

def display_statistics():
    db = DatabaseManager()
    total_books, read_books, read_percentage = db.get_statistics()
    print(f"Total Books: {total_books}")
    print(f"Books Read: {read_books}")
    print(f"Percentage Read: {read_percentage:.2f}%")

if __name__ == "__main__":
    db = DatabaseManager()  # ✅ Ensure database creation

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "add":
            add_book_from_cli()
        elif command == "search":
            search_books_from_cli()
        elif command == "update":
            update_book_from_cli()
        elif command == "delete":
            delete_book_from_cli()
        elif command == "display":
            list_books()
        elif command == "stats":
            display_statistics()
        else:
            print("❌ Invalid command. Use: add_book, search, update_book, delete_book, list_books, or stats")
    else:
        print("Usage: python database.py <command>")
