class Library:
    def __init__(self, id, books_ids, nb_books_N, nb_books_per_day_M, time_sign_T):
        self.id = id
        self.books_ids = set(books_ids)
        self.nb_books_N = nb_books_N
        self.nb_books_per_day_M = nb_books_per_day_M
        self.time_sign_T = time_sign_T
        self.score = 0
        self.scanned_books = []
        self.coefficient = 0

    def update_books(self, books_taken):
        self.books_ids = self.books_ids.difference(books_taken)
    
    def update_score(self, books_scores):
        self.score = sum(books_scores[b] for b in self.books_ids)

    def update_coefficient(self):
        self.coefficient = self.score / self.time_sign_T
    
    def update(self, books_taken, books_scores):
        self.update_books(books_taken)
        self.update_score(books_scores)
        self.update_coefficient()
    
    def sort_books_by_score(self, books_scores, reverse=True):
        self.books_ids = set(sorted(self.books_ids, key=lambda o: books_scores[o], reverse=reverse))

    def consolidate_book_search(self, book_search):
        for book_id in self.books_ids:
            book_search[book_id].append(self)

    def display(self):
        print("Books ids:", self.books_ids)
        print("Number of books (N):", self.nb_books_N)
        print("Number of books per day (M):", self.nb_books_per_day_M)
        print("Time to sign (T):", self.time_sign_T)
