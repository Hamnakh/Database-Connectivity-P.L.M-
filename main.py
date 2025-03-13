import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from database import DatabaseManager
import datetime

class LibraryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Library Manager")
        self.root.geometry("1000x600")
        self.db = DatabaseManager()
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=25)
        
        self.create_widgets()
        self.load_books()

    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.search_books())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=5)

        # Book list
        columns = ("ID", "Title", "Author", "Category", "Status")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("ID", width=50)
        self.tree.column("Title", width=300)
        self.tree.column("Author", width=200)
        self.tree.column("Category", width=150)
        self.tree.column("Status", width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Book", command=self.show_add_book_dialog).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit Book", command=self.show_edit_book_dialog).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Book", command=self.delete_book).pack(side="left", padx=5)

        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def load_books(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load books from database
        books = self.db.get_all_books()
        for book in books:
            self.tree.insert("", "end", values=(book[0], book[1], book[2], book[4], book[5]))

    def search_books(self):
        query = self.search_var.get()
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Search books
        books = self.db.search_books(query)
        for book in books:
            self.tree.insert("", "end", values=(book[0], book[1], book[2], book[4], book[5]))

    def show_add_book_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()

        # Create and pack widgets
        ttk.Label(dialog, text="Title:").pack(pady=5)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.pack(pady=5)

        ttk.Label(dialog, text="Author:").pack(pady=5)
        author_entry = ttk.Entry(dialog, width=40)
        author_entry.pack(pady=5)

        ttk.Label(dialog, text="ISBN:").pack(pady=5)
        isbn_entry = ttk.Entry(dialog, width=40)
        isbn_entry.pack(pady=5)

        ttk.Label(dialog, text="Category:").pack(pady=5)
        category_entry = ttk.Entry(dialog, width=40)
        category_entry.pack(pady=5)

        ttk.Label(dialog, text="Status:").pack(pady=5)
        status_var = tk.StringVar(value="To Read")
        status_combo = ttk.Combobox(dialog, textvariable=status_var, 
                                  values=["To Read", "Reading", "Completed"])
        status_combo.pack(pady=5)

        ttk.Label(dialog, text="Notes:").pack(pady=5)
        notes_text = tk.Text(dialog, width=40, height=5)
        notes_text.pack(pady=5)

        def save_book():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            
            if not title or not author:
                messagebox.showerror("Error", "Title and Author are required!")
                return
                
            self.db.add_book(
                title=title,
                author=author,
                isbn=isbn_entry.get().strip(),
                category=category_entry.get().strip(),
                status=status_var.get(),
                notes=notes_text.get("1.0", "end-1c")
            )
            self.load_books()
            dialog.destroy()

        ttk.Button(dialog, text="Save", command=save_book).pack(pady=20)

    def show_edit_book_dialog(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a book to edit!")
            return

        book_id = self.tree.item(selected_items[0])['values'][0]
        book = self.db.get_book_by_id(book_id)

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Book")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()

        # Create and pack widgets
        ttk.Label(dialog, text="Title:").pack(pady=5)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.insert(0, book[1])
        title_entry.pack(pady=5)

        ttk.Label(dialog, text="Author:").pack(pady=5)
        author_entry = ttk.Entry(dialog, width=40)
        author_entry.insert(0, book[2])
        author_entry.pack(pady=5)

        ttk.Label(dialog, text="ISBN:").pack(pady=5)
        isbn_entry = ttk.Entry(dialog, width=40)
        isbn_entry.insert(0, book[3] if book[3] else "")
        isbn_entry.pack(pady=5)

        ttk.Label(dialog, text="Category:").pack(pady=5)
        category_entry = ttk.Entry(dialog, width=40)
        category_entry.insert(0, book[4] if book[4] else "")
        category_entry.pack(pady=5)

        ttk.Label(dialog, text="Status:").pack(pady=5)
        status_var = tk.StringVar(value=book[5])
        status_combo = ttk.Combobox(dialog, textvariable=status_var, 
                                  values=["To Read", "Reading", "Completed"])
        status_combo.pack(pady=5)

        ttk.Label(dialog, text="Notes:").pack(pady=5)
        notes_text = tk.Text(dialog, width=40, height=5)
        notes_text.insert("1.0", book[7] if book[7] else "")
        notes_text.pack(pady=5)

        def update_book():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            
            if not title or not author:
                messagebox.showerror("Error", "Title and Author are required!")
                return
                
            self.db.update_book(
                book_id=book_id,
                title=title,
                author=author,
                isbn=isbn_entry.get().strip(),
                category=category_entry.get().strip(),
                status=status_var.get(),
                notes=notes_text.get("1.0", "end-1c")
            )
            self.load_books()
            dialog.destroy()

        ttk.Button(dialog, text="Update", command=update_book).pack(pady=20)

    def delete_book(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a book to delete!")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
            book_id = self.tree.item(selected_items[0])['values'][0]
            self.db.delete_book(book_id)
            self.load_books()

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Using a modern theme
    app = LibraryManager(root)
    root.mainloop() 