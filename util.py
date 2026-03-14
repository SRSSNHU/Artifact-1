class BookRepository:
    """Responsible for storing and retrieving book data"""

    def __init__(self):
        self.books = {}

    def add(self, book_id, title):
        self.books[book_id] = {'title': title, 'available': True}

    def get(self, book_id):
        return self.books.get(book_id)
    
    def set_availability(self, book_id, available):
        self.books[book_id]['available'] = available

    def all(self):
        return self.books

class MemberRepository:
    """Responsible for storing and retrieving member data."""

    def __init__(self):
        self.members = {}

    def add(self, member_id, name, email):
        self.members[member_id] = {'name': name, 'email': email}

    def get(self, member_id):
        return self.members.get(member_id)
    
    def all(self):
        return self.members
    
class LoanRepository:
    """Responsible for storing and retrieving loan data."""

    def __init__(self):
        self.loans = {}

    def add(self, book_id, member_id):
        self.loans[book_id] = member_id

    def all(self):
        return self.loans
    
class FeeCalculator:
    """Responsible for calculating loan-related fees."""

    daily_rate = 1.50

    def calculate_late_fee(self, days_late):
        return days_late * self.daily_rate
    
class NotificationService:
    """Responsible for sending notifications to memebrs."""

    def send_email(self, email, message):
        print(f'Email sent to {email}: {message}')

class LoanService:
    """Responsible for checkout business logic."""

    def __init__(self, books, members, loans, fee_calculator, notifier):
        self.books = books
        self.members = members
        self.loans = loans
        self.fee_calculator = fee_calculator
        self.notifier = notifier

    def checkout(self, book_id, member_id, days_late):
        book = self.books.get(book_id)
        member = self.members.get(member_id)

        if not book:
            raise ValueError('Book not found.')
        if not member:
            raise ValueError('Member not found.')
        if not book['available']:
            raise ValueError('Book is not available.')
        
        fee = self.fee_calculator.calculate_late_fee(days_late)
        self.books.set_availability(book_id, False)
        self.loans.add(book_id, member_id)

        self.notifier.send_email(member['email'], f"You checked out '{book['title']}'. Fee: ${fee:.2f}")

class ReportGenerator:
    """Responsible for generating library reports"""

    def __init__(self, books, members, loans):
        self.books = books
        self.members = members
        self.loans = loans

    def generate(self):
        print('\n--- Library Report ---')
        self._print_books()
        self._print_members()
        self._print_loans()
        print()

    def _print_books(self):
        print('\nBooks:')
        books = self.books.all()
        if not books:
            print(' No books available')
            return
        for book_id, info in books.items():
            status = 'Available' if info['available'] else 'Checked Out'
            print(f'  ID: {book_id} | Title: {info['title']} | Status: {status}')

    def _print_members(self):
        print('\nMembers:')
        members = self.members.all()
        if not members:
            print('  No members registered.')
            return
        for member_id, info in members.items():
            print(f'  ID: {member_id} | Name: {info['name']} | Email: {info['email']}')

    def _print_loans(self):
        print('\nActive Loans:')
        loans = self.loans.all()
        if not loans:
            print('  No active loans.')
            return
        for book_id, member_id in loans.items():
            title = self.books.get(book_id)['title']
            name = self.members.get(member_id)['name']
            print(f"  '{title}' checked out by {name}")

class LibraryConsoleUI:
    """Responsible for all user input/output interaction."""

    def __init__(self, books, members, loan_service, reporter):
        self.books = books
        self.members = members
        self.loan_service = loan_service
        self.reporter = reporter

    def prompt_add_book(self):
        book_id = input('Enter book ID: ')
        title = input('Enter book title: ')
        self.books.add(book_id, title)
        print('Book added successfully.\n')

    def prompt_register_member(self):
        member_id = input('Enter member ID: ')
        name = input('Enter member name: ')
        email = input('Enter member email: ')
        self.members.add(member_id, name, email)
        print('Member registered successfully.\n')

    def prompt_checkout(self):
        book_id = input('Enter book ID: ')
        member_id = input('Enter member ID: ')
        days_late = int(input('Enter days late (0 if none): '))
        try:
            self.loan_service.checkout(book_id, member_id, days_late)
            print('Checkout complete.\n')
        except ValueError as e:
            print(f'prompt_checkout error: {e}\n')

    def run(self):
        while True:
            print('1. Add Book')
            print('2. Register Member')
            print('3. Checkout Book')
            print('4. Generate Report')
            print('5. Exit')

            choice = input('Choose an option: ')

            if choice == '1':
                self.prompt_add_book()
            elif choice == '2':
                self.prompt_register_member()
            elif choice == '3':
                self.prompt_checkout()
            elif choice == '4':
                self.reporter.generate()
            elif choice == '5':
                break
            else:
                print('Invalid option. Please try again.\n')