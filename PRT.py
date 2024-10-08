import mysql.connector
conn = mysql.connector.connect (
    host = "localhost",
    user = "root", 
    passwd = "Tamanna"
)

c = conn.cursor()
c.execute("CREATE DATABASE if not exists reading_tracker")
c.execute("USE reading_tracker")

sql1 = "create table if not exists books (id int auto_increment primary key, title varchar(100) not null, author varchar(50), genre varchar(50), read_status tinyint(1), user varchar(30), foreign key (user) references users(name))"
sql2 = "create table if not exists users (name varchar(30) not null primary key)"
c.execute(sql2)
c.execute(sql1)
conn.commit()

class Book:
    def __init__ (self, title, author, genre, read_status, user):
        self.title = title
        self.author = author
        self.genre = genre
        self.read_status = read_status
        self.user = user
    
class User:
    def __init__ (self, name):
        self.name = name
    
    def add_book (self, book):
        sql = "INSERT INTO books (title, author, genre, read_status, user) SELECT %s, %s, %s, %s, %s WHERE NOT EXISTS(SELECT title, user FROM books WHERE title = %s and user = %s);"
        val = (book.title, book.author, book.genre, book.read_status, self.name, book.title, self.name)
        try:
            c.execute(sql, val)
        except:
            print('Book already exists in your reading list')
        conn.commit()
        print(f"{book.title} added to reading list")

    def update_status (self, book, read_status):
        sql_update = 'update books set read_status = %s where user = %s and title = %s'
        c.execute(sql_update, (read_status, self.name, book,))
        print(f"{Book}'s read status was updated!")
        conn.commit()

    def view_list(self):
        print(f"\n{self.name}'s Books List: ")
        sql = 'select * from books where user = %s'
        c.execute(sql, (self.name,))
        for book in c.fetchall():
            (id, title, author, genre, read_status, user) = book
            print(f"Title: {title}\n Author: {author}\n Genre: {genre}\n Read Status: {read_status}\n")

    def remove_book (self, title):
        sql = 'delete from books where title = %s'
        try: 
            c.execute(sql, (title,))
        except:
            print('Book does not exist in your reading list')
        print(f"{title} was removed from your reading list")
        conn.commit()

    def check_book(self, title):
        sql_check_book = 'select title from books where title = %s and user = %s'
        c.execute(sql_check_book, (title, self.name,))
        result = c.fetchall()
        return result

def add_book(user):
    title = input("Enter the book title: ").title()
    author = input("Enter the author's name: ").title()
    genre = input("Enter the genre of the book: ").lower()
    while (True):
        try:
            read_status = int(input("Enter '0' if you want to read the book, or '1' if you have already read it: "))
        except:
            pass
        if read_status in [0,1]:
            break
        else:
            print("Invalid read status. Try again.")
    sql_check_user = "select * from users where name = %s"
    c.execute(sql_check_user, (user.name,))
    result = c.fetchone()
    if not result:
        sql_insert_user = "insert into users (name) values (%s)"
        c.execute(sql_insert_user, (user.name,))
        conn.commit()
        print(f"User {user.name} inserted into the database")
    book = Book(title, author, genre, read_status, user)
    user.add_book(book)

def check_book(user):
    title = input("Enter the title of the book to be removed: ").title()
    result = user.check_book(title)
    if result:
        sql = 'select * from books where user = %s and title = %s'
        c.execute(sql, (user.name, title,))
        for i in c.fetchall():
            (id, title, *rest) = i
            print(f'{title} was found in your reading list')
    else:
        print(f'{title} is not present in your reading list')
        
def view_list(user):
    user.view_list()

def remove_book(user):
    title = input("Enter the title of the book to be removed: ").title()
    res = user.check_book(title)
    if not res:
        print(f'{title} is not in your reading list. Please add it instead')
        return
    user.remove_book(title)

def update_status(user):
    title = input("Enter the title of the book: ").title()
    res = user.check_book(title)
    if not res:
        print(f'{title} is not in your reading list. Please add it instead')
        return
    while(True):
        try:
            r_s = int(input("Have you read this book? (0: No or 1: Yes) "))
        except:
            pass
        if r_s in [0,1]:
            break
        else:
            print("Invalid entry, try again")
    user.update_status(title, r_s)

def main():
    name = input('Enter your name: ').title()
    user = User(name)
    while True:
        print("1. View List")
        print("2. Add Book")
        print("3. Remove Book")
        print("4. Update Book")
        print("5. Find Book")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_list(user)
        elif choice == '2':
            add_book(user)
        elif choice == '3':
            remove_book(user)
        elif choice == '4':
            update_status(user)
        elif choice == '5':
            check_book(user)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()