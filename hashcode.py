import os
import sys
from collections import defaultdict

from library import Library

books_taken = set()
libs_taken = []
books_scores = {}
book_search = defaultdict(list)

##############
# Read input #
##############

filename = sys.argv[1]

f = open(filename)
# Ger number of books, libs, days
nb_books_B, nb_libs_L, deadline_D = (int(n) for n in f.readline().split())

# Get books scores
books = f.readline().split()
books_scores = dict([(i, int(books[i])) for i in range(len(books))])

libraries = []
for i in range(nb_libs_L):
    nb_books_N, time_sign_T, nb_books_per_day_M = (int(n) for n in f.readline().split())
    books_ids = [int(n) for n in f.readline().split()]
    lib = Library(i, books_ids, nb_books_N, nb_books_per_day_M, time_sign_T)
    lib.update_score(books_scores)
    lib.update_coefficient()
    lib.sort_books_by_score(books_scores)
    lib.consolidate_book_search(book_search)
    libraries.append(lib)
f.close()

##########
# Output #
##########

name, ext = os.path.splitext(filename)
output_filename = ''.join([name, '_output', ext])


# Print summary
if '-v' in sys.argv:
    print("Number of books (B):", nb_books_B)
    print("Number of libraries (L):", nb_libs_L)
    print("Deadline (D):", deadline_D)

    print("Books scores:", books_scores)

    print("Libraries:")
    for lib in libraries:
        lib.display()
        print('----------')

# Sort libraries by coefficient
libraries_chosen = []
libraries = sorted(libraries, key=lambda o: o.coefficient, reverse=True)
days = deadline_D
while days > 0 and len(libraries) > 0:
    l = libraries.pop(0)
    if days - l.time_sign_T < 0:
        continue
    days -= l.time_sign_T
    libraries_chosen.append(l)
    if len(l.books_ids) < days*l.nb_books_per_day_M:
        l.scanned_books = set(list(l.books_ids)[:days*l.nb_books_per_day_M])
        books_taken = books_taken.union(l.scanned_books)
    else:
        l.scanned_books = l.books_ids
        books_taken = books_taken.union(l.scanned_books)
    for lib in libraries:
        lib.update(books_taken, books_scores)
    libraries = sorted(libraries, key=lambda o: o.coefficient, reverse=True)
    print(days)

print(f"Final score: {sum([books_scores[b] for b in books_taken])}")


with open(output_filename, "w") as f:
    f.write(f"{len(libraries_chosen)}\n")
    for l in libraries_chosen:
        f.write(f"{l.id} {len(l.scanned_books)}\n")
        f.write(" ".join([str(x) for x in l.scanned_books]))
        f.write("\n")
