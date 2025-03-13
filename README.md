# Personal Library Manager (Bayt al-Hikma)

A sophisticated personal library management system with database connectivity. This application helps you manage your personal book collection with features like adding, updating, deleting, and searching books.

## Features

- Modern GUI interface using tkinter and ttkthemes
- SQLite database for efficient data storage
- CRUD operations (Create, Read, Update, Delete) for books
- Search functionality
- Book categorization
- Reading status tracking

## Setup Instructions

1. Ensure you have Python 3.8+ installed
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

## Database Schema

The application uses SQLite with the following schema:

- Books Table:
  - id (PRIMARY KEY)
  - title
  - author
  - isbn
  - category
  - status (Reading/Completed/To Read)
  - added_date
  - notes

## Usage

1. Launch the application
2. Use the "Add Book" button to add new books
3. Select a book from the list to view/edit details
4. Use the search bar to find specific books
5. Right-click on books for additional options 