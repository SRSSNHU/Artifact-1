from util import BookRepository, MemberRepository, FeeCalculator, NotificationService, LoanRepository, LoanService, ReportGenerator, LibraryConsoleUI

def main():
    books = BookRepository()
    members = MemberRepository()
    loans = LoanRepository()

    fee_calculator = FeeCalculator()
    notifer = NotificationService()
    loan_service = LoanService(books, members, loans, fee_calculator, notifer)
    reporter = ReportGenerator(books, members, loans)

    ui = LibraryConsoleUI(books, members, loan_service, reporter)
    ui.run()

if __name__ == "__main__":
    main()