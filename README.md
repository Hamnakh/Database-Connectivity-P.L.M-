# Personal Library Manager

A powerful personal library management system with database connectivity. This application allows you to efficiently manage your book collection, track reading progress, and generate statistics.

## Features

- **Command-line Interface (CLI)** for managing books easily.
- **SQLite Database** for persistent data storage.
- **CRUD Operations:** Add, update, delete, and search books.
- **Reading Progress Tracking** (Read/Unread status).
- **Book Statistics:** View total books, books read, and percentage read.

## Setup Instructions

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Install Dependencies
No external dependencies are required for this project. It runs using Python’s built-in SQLite module.

### 3. Running the Application
To execute the script, open a terminal and navigate to the project folder:

```sh
python database.py <command>
```

### 4. Available Commands

| Command        | Description                                |
|---------------|--------------------------------------------|
| `add`    | Add a new book to the library.            |
| `search`      | Search books by title, author, or genre.  |
| `update` | Update an existing book’s details.        |
| `delete` | Remove a book from the library.           |
| `display`  | Display all books in the collection.      |
| `stats`       | Show total books, books read, and progress. |

## Database Schema

The application uses an SQLite database (`library.db`) with the following table structure:

- **Books Table:**
  - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
  - `title` (TEXT, NOT NULL)
  - `author` (TEXT, NOT NULL)
  - `publication_year` (INTEGER)
  - `genre` (TEXT)
  - `read_status` (BOOLEAN, DEFAULT 0)

## Usage Guide

1. **Adding a Book:**
   ```sh
   python database.py add
   ```
   Follow the prompts to enter book details.

2. **Searching for Books:**
   ```sh
   python database.py search
   ```
   Enter keywords to find books by title, author, or genre.

3. **Updating a Book:**
   ```sh
   python database.py update
   ```
   Enter the Book ID and modify details as required.

4. **Deleting a Book:**
   ```sh
   python database.py delete
   ```
   Enter the Book ID to remove it from the database.

5. **Viewing All Books:**
   ```sh
   python database.py display
   ```
   Displays a list of all books in the collection.

6. **Viewing Statistics:**
   ```sh
   python database.py stats
   ```
   Shows total books, books read, and percentage read.

## License
This project is open-source and free to use under the MIT License.

---
Enjoy managing your personal library with ease! 📚