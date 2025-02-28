import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
from datetime import datetime, timedelta
from PIL import Image, ImageTk  # Import modul yang diperlukan



class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        # Load books and borrowers from CSV
        self.books = self.load_books()
        self.borrowers = self.load_borrowers()

         # Tampilkan gambar sebagai latar belakang
        self.background_image = Image.open("background 1.jpg")  # Ganti dengan nama file gambar Anda
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Sort books initially by category and title
        self.books.sort(key=lambda x: (x['title']))

        # Create GUI components
        self.create_widgets()
        self.populate_books()

    def load_books(self):
        books = []
        try:
            with open('books.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    books.append(row)
        except FileNotFoundError:
            messagebox.showerror("Error", "books.csv not found")
        return books

    def load_borrowers(self):
        borrowers = []
        try:
            with open('borrowers.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    borrowers.append(row)
        except FileNotFoundError:
            messagebox.showerror("Error", "borrowers.csv not found")
        return borrowers

    def create_widgets(self):
        # Filter options
        tk.Label(self.root, text="Filter by:", bg= "#FFFDD0").grid(row=0, column=0, padx=5, pady=5)
        self.filter_var = tk.StringVar(value="All")
        filter_options = ttk.Combobox(self.root, textvariable=self.filter_var, values=["All", "ID", "Category", "Genre", "Year", "Author"])
        filter_options.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Apply", command=self.filter_books).grid(row=0, column=2, padx=5, pady=5)

        # Search bar
        self.search_var = tk.StringVar()
        tk.Label(self.root, text="Search:", bg= "#FFFDD0").grid(row=0, column=3, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.search_var).grid(row=0, column=4, padx=5, pady=5)
        tk.Button(self.root, text="Search", command=self.search_books).grid(row=0, column=5, padx=5, pady=5)

        # Genre selection
        tk.Label(self.root, text="Genre:", bg= "#FFFDD0").grid(row=0, column=6, padx=5, pady=5)
        self.genre_var = tk.StringVar(value="All")
        genres = ["All"] + sorted(set(book['genre'] for book in self.books))
        genre_options = ttk.Combobox(self.root, textvariable=self.genre_var, values=genres)
        genre_options.grid(row=0, column=7, padx=5, pady=5)
        tk.Button(self.root, text="Apply", command=self.filter_books).grid(row=0, column=8, padx=5, pady=5)

        # Books list
        self.tree = ttk.Treeview(self.root, columns=("ID", "Title", "Category", "Genre", "Author", "Year", "Count"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Count", text="Count")
        self.tree.column("ID", width=50, stretch=tk.YES)  # Adjusted width to show the ID column
        self.tree.grid(row=1, column=0, columnspan=9, padx=5, pady=5)

        # Add, Borrow, and Return buttons
        tk.Button(self.root, text="Add Book", command=self.add_book).grid(row=2, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="Borrow", command=self.borrow_book).grid(row=2, column=3, columnspan=3, pady=10)
        tk.Button(self.root, text="Return", command=self.return_book).grid(row=2, column=6, columnspan=3, pady=10)

        # Show Borrowers button
        tk.Button(self.root, text="Show Borrowers", command=self.show_borrowers).grid(row=3, column=0, columnspan=9, pady=10)

    def populate_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for book in self.books:
            self.tree.insert("", tk.END, values=(book['id'], book['title'], book['category'], book['genre'], book['author'], book['year'], book['count']))

    def search_books(self):
        query = self.search_var.get().lower()
        genre_filter = self.genre_var.get()
        filtered_books = [book for book in self.books if (query in book['title'].lower() or query in book['author'].lower()) and (genre_filter == "All" or book['genre'] == genre_filter)]
        self.populate_filtered_books(filtered_books)

    def populate_filtered_books(self, books):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for book in books:
            self.tree.insert("", tk.END, values=(book['id'], book['title'], book['category'], book['genre'], book['author'], book['year'], book['count']))

    def filter_books(self):
        filter_by = self.filter_var.get()
        genre_filter = self.genre_var.get()
        if filter_by == "ID":
            filtered_books = sorted(self.books, key=lambda x: int(x['id']))
        elif filter_by == "Category":
            filtered_books = sorted(self.books, key=lambda x: (x['category'], x['title']))
        elif filter_by == "Genre":
            filtered_books = sorted(self.books, key=lambda x: (x['genre'], x['title']))
        elif filter_by == "Year":
            filtered_books = sorted(self.books, key=lambda x: (x['year'], x['title']))
        elif filter_by == "Author":
            filtered_books = sorted(self.books, key=lambda x: (x['author'], x['title']))
        else:
            filtered_books = sorted(self.books, key=lambda x: (x['title']))
        
        if genre_filter != "All":
            filtered_books = [book for book in filtered_books if book['genre'] == genre_filter]
        
        self.populate_filtered_books(filtered_books)

    def add_book(self):
        # Dialog for adding a new book
        add_book_dialog = tk.Toplevel(self.root)
        add_book_dialog.title("Add New Book")
        add_book_dialog.configure(bg="#FFFDD0")  # Background color set to Chocolate Delight

        # Book ID
        tk.Label(add_book_dialog, text="ID:", bg= "#FFFDD0").grid(row=0, column=0, padx=5, pady=5)
        id_entry = tk.Entry(add_book_dialog)
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Book Title
        tk.Label(add_book_dialog, text="Title:", bg= "#FFFDD0").grid(row=1, column=0, padx=5, pady=5)
        title_entry = tk.Entry(add_book_dialog)
        title_entry.grid(row=1, column=1, padx=5, pady=5)

        # Book Category
        tk.Label(add_book_dialog, text="Category:", bg= "#FFFDD0").grid(row=2, column=0, padx=5, pady=5)
        category_entry = tk.Entry(add_book_dialog)
        category_entry.grid(row=2, column=1, padx=5, pady=5)

        # Book Genre
        tk.Label(add_book_dialog, text="Genre:", bg= "#FFFDD0").grid(row=3, column=0, padx=5, pady=5)
        genre_entry = tk.Entry(add_book_dialog)
        genre_entry.grid(row=3, column=1, padx=5, pady=5)

        # Book Author
        tk.Label(add_book_dialog, text="Author:", bg= "#FFFDD0").grid(row=4, column=0, padx=5, pady=5)
        author_entry = tk.Entry(add_book_dialog)
        author_entry.grid(row=4, column=1, padx=5, pady=5)

        # Book Year
        tk.Label(add_book_dialog, text="Year:", bg= "#FFFDD0").grid(row=5, column=0, padx=5, pady=5)
        year_entry = tk.Entry(add_book_dialog)
        year_entry.grid(row=5, column=1, padx=5, pady=5)

        # Book Count
        tk.Label(add_book_dialog, text="Count:", bg= "#FFFDD0").grid(row=6, column=0, padx=5, pady=5)
        count_entry = tk.Entry(add_book_dialog)
        count_entry.grid(row=6, column=1, padx=5, pady=5)

        def save_new_book():
            new_book = {
                'id': id_entry.get(),
                'title': title_entry.get(),
                'category': category_entry.get(),
                'genre': genre_entry.get(),
                'author': author_entry.get(),
                'year': year_entry.get(),
                'count': count_entry.get()
            }
            self.books.append(new_book)
            self.populate_books()
            self.save_books()
            add_book_dialog.destroy()

        tk.Button(add_book_dialog, text="Add", command=save_new_book).grid(row=7, column=0, columnspan=2, pady=10)

    def borrow_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            book_id = self.tree.item(selected_item[0], 'values')[0]

            # Dialog for borrower name and NIM
            borrow_dialog = tk.Toplevel(self.root)
            borrow_dialog.title("Borrow Book")
            borrow_dialog.configure(bg= "#FFFDD0")  # Background color set to Chocolate Delight

            # Entry for borrower name
            tk.Label(borrow_dialog, text="Enter borrower name:", bg= "#FFFDD0").grid(row=0, column=0, padx=5, pady=5)
            name_entry = tk.Entry(borrow_dialog)
            name_entry.grid(row=0, column=1, padx=5, pady=5)

            # Entry for borrower NIM
            tk.Label(borrow_dialog, text="Enter NIM:", bg="#FFFDD0").grid(row=1, column=0, padx=5, pady=5)
            nim_entry = tk.Entry(borrow_dialog)
            nim_entry.grid(row=1, column=1, padx=5, pady=5)

            def borrow():
                borrower_name = name_entry.get()
                nim = nim_entry.get()
                if borrower_name and nim:
                    for book in self.books:
                        if book['id'] == book_id:
                            if int(book['count']) > 0:
                                book['count'] = str(int(book['count']) - 1)
                                borrow_date = datetime.now().strftime("%Y-%m-%d")
                                return_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                                self.borrowers.append({'book_id': book_id, 'borrower_name': borrower_name, 'nim': nim, 'borrow_date': borrow_date, 'return_date': return_date})
                                self.populate_books()
                                self.save_books()
                                self.save_borrowers()
                                borrow_dialog.destroy()  # Close the dialog after borrowing
                            else:
                                messagebox.showwarning("Warning", "No more copies available to borrow")
                            return

            # Button to borrow the book
            tk.Button(borrow_dialog, text="Borrow", command=borrow, bg= "#FFFDD0").grid(row=2, columnspan=2, padx=5, pady=5)
    def return_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            book_id = self.tree.item(selected_item[0], 'values')[0]
            for book in self.books:
                if book['id'] == book_id:
                    book['count'] = str(int(book['count']) + 1)
                    # Find the borrower who borrowed this book
                    borrower = None
                    for b in self.borrowers:
                        if b['book_id'] == book_id:
                            borrower = b
                            break
                    if borrower:
                        # Calculate overdue days
                        return_date = datetime.strptime(borrower['return_date'], "%Y-%m-%d")
                        today = datetime.now()
                        overdue_days = max(0, (today - return_date).days)
                        if overdue_days > 0:
                            # Calculate and show the fine
                            fine = overdue_days * 1000  # Assuming 1000 rupiah per day fine
                            messagebox.showinfo("Overdue", f"You returned the book {overdue_days} days late. You need to pay a fine of {fine} rupiah.")
                        else:
                            messagebox.showinfo("Return Book", "Book returned successfully.")
                        # Remove borrower from borrowers list
                        self.borrowers.remove(borrower)
                    else:
                        messagebox.showwarning("Warning", "No borrower found for this book.")
                    self.populate_books()
                    self.save_books()
                    self.save_borrowers()
                    return

    def show_borrowers(self):
        borrowers_window = tk.Toplevel(self.root)
        borrowers_window.title("Borrowers List")
        borrowers_window.configure(bg= "#FFFDD0")  # Background color set to Chocolate Delight

        borrowers_tree = ttk.Treeview(borrowers_window, columns=("Book ID", "Borrower Name", "NIM", "Borrow Date", "Return Date"), show='headings')
        borrowers_tree.heading("Book ID", text="Book ID")
        borrowers_tree.heading("Borrower Name", text="Borrower Name")
        borrowers_tree.heading("NIM", text="NIM")
        borrowers_tree.heading("Borrow Date", text="Borrow Date")
        borrowers_tree.heading("Return Date", text="Return Date")
        borrowers_tree.pack(fill=tk.BOTH, expand=True)

        for borrower in self.borrowers:
            borrowers_tree.insert("", tk.END, values=(borrower['book_id'], borrower['borrower_name'], borrower['nim'], borrower['borrow_date'], borrower['return_date']))
            borrowers_tree.configure(bg="#f5deb3")  # Set background color for the borrowers treeview
            borrowers_tree.tag_configure("evenrow", background="#fff8dc")  # Set background color for even rows
            borrowers_tree.tag_configure("oddrow", background="#fafad2")  # Set background color for odd rows

        # Alternate row colors
        for i, borrower in enumerate(self.borrowers):
            if i % 2 == 0:
                borrowers_tree.insert("", tk.END, values=(borrower['book_id'], borrower['borrower_name'], borrower['nim'], borrower['borrow_date'], borrower['return_date']), tags=("evenrow",))
            else:
                borrowers_tree.insert("", tk.END, values=(borrower['book_id'], borrower['borrower_name'], borrower['nim'], borrower['borrow_date'], borrower['return_date']), tags=("oddrow",))

    def save_books(self):
        with open('books.csv', 'w', newline='') as csvfile:
            fieldnames = ['id', 'title', 'category', 'genre', 'author', 'year', 'count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for book in self.books:
                writer.writerow(book)

    def save_borrowers(self):
        with open('borrowers.csv', 'w', newline='') as csvfile:
            fieldnames = ['book_id', 'borrower_name', 'nim', 'borrow_date', 'return_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for borrower in self.borrowers:
                writer.writerow(borrower)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#d2691e")  # Set background color for the root window
    app = LibraryManagementSystem(root)
    root.mainloop()


