from main import Book, db, Publisher, Author, Genre
book1 = Book('Good Omens', 8, 1)
book2 = Book('Heads You Lose', 9, 1)
book3 = Book('Between the Lines', 7, 2)
author1 = Author('Neil', 'Gaiman')
author2 = Author('Terry', 'Pratchett')
author3 = Author('Lisa', 'Lutz')
author4 = Author('Jodi', 'Picoult')
genre1 = Genre('Fantasy')
genre2 = Genre('Criminal')
db.session.add_all([book1, book2, book3, author1, author2, author3, author4, genre1, genre2])
db.session.commit()

# append authors to books

good_omens = Book.query.filter_by(title='Good Omens').first()
neil_gaiman = Author.query.filter_by(fname='Neil').first()
terry_pratchnett = Author.query.filter_by(fname='Terry').first()
good_omens.authors.append(neil_gaiman)
good_omens.authors.append(terry_pratchnett)
good_omens.authors
#[Neil Gaiman, Terry Pratchett]
neil_gaiman.books
# [Good Omens 8]
terry_pratchnett.books
# [Good Omens 8]

#Append books to authors

between_the_lines = Book.query.filter_by(title='Between the Lines').first()
author_jp = Author.query.filter_by(fname='Jodi').first()
author_jp.books.append(between_the_lines)
terry_pratchnett.books.append(between_the_lines)
terry_pratchnett.books
# [Good Omens 8, Between the Lines 7]

#append genres

fantasy = Genre.query.filter_by(genre='Fantasy').first()
criminal = Genre.query.filter_by(genre='Criminal').first()
fantasy.books.append(good_omens)
between_the_lines.genres.append(criminal)
criminal.books
# [Between the Lines 7, Heads You Lose 9]
fantasy.books
# [Good Omens 8]

books = Book.query.all()
for i in books:
    print(i, i.publisher, i.genres, i.authors)

# Good Omens 8 Baltos Lankos [Fantasy] [Neil Gaiman, Terry Pratchett]
# Heads You Lose 9 Baltos Lankos [Criminal] [Lisa Lutz]
# Between the Lines 7 Alma Littera [Criminal] [Jodi Picoult, Terry Pratchett]

genres = Genre.query.all()
for i in genres:
     print(i, i.books)

# Fantasy [Good Omens 8]
# Criminal [Between the Lines 7, Heads You Lose 9]