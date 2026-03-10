class LibraryManager:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.loans = {}

    def add_book(self):
        book_id = input("Enter book ID: ")
        title = input("Enter book title: ")
        self.books[book_id] = {"title": title, "available": True}
        print("Book added successfully.\n")

    def register_member(self):
        member_id = input("Enter member ID: ")
        name = input("Enter member name: ")
        email = input("Enter member email: ")
        self.members[member_id] = {"name": name, "email": email}
        print("Member registered successfully.\n")

    def checkout_book(self):
        book_id = input("Enter book ID: ")
        member_id = input("Enter member ID: ")

        if book_id not in self.books:
            print("Book not found.\n")
            return
        if member_id not in self.members:
            print("Member not found.\n")
            return
        if not self.books[book_id]["available"]:
            print("Book not available.\n")
            return

        days_late = int(input("Enter days late (0 if none): "))
        fee = self.calculate_late_fee(days_late)

        self.books[book_id]["available"] = False
        self.loans[book_id] = member_id

        self.send_email(
            self.members[member_id]["email"],
            f"You checked out '{self.books[book_id]['title']}'. Fee: ${fee}"
        )
        print("Checkout complete.\n")

    def calculate_late_fee(self, days_late):
        return days_late * 1.50

    def send_email(self, email, message):
        print(f"(Email sent to {email}): {message}")

    def generate_report(self):
        print("\n--- Library Report ---")

        print("\nBooks:")
        if not self.books:
            print("  No books available.")
        else:
            for book_id, info in self.books.items():
                status = "Available" if info["available"] else "Checked Out"
                print(f"  ID: {book_id} | Title: {info['title']} | Status: {status}")

        print("\nMembers:")
        if not self.members:
            print("  No members registered.")
        else:
            for member_id, info in self.members.items():
                print(f"  ID: {member_id} | Name: {info['name']} | Email: {info['email']}")

        print("\nActive Loans:")
        if not self.loans:
            print("  No active loans.")
        else:
            for book_id, member_id in self.loans.items():
                title = self.books[book_id]["title"]
                name = self.members[member_id]["name"]
                print(f"  '{title}' checked out by {name}")

        print()


def main():
    library = LibraryManager()

    while True:
        print("1. Add Book")
        print("2. Register Member")
        print("3. Checkout Book")
        print("4. Generate Report")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.register_member()
        elif choice == "3":
            library.checkout_book()
        elif choice == "4":
            library.generate_report()
        elif choice == "5":
            break
        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()

