#!/user/bin/env python3
# -*- coding: utf-8 -*-
from Config import Book, ReturnCode, db


class BookServices:

    ## insert ##
    @staticmethod
    def insert_book(new_book):
        insert_book = Book(
            title=new_book.title,
            author=new_book.author,
            category_id=new_book.category_id,
            publisher=new_book.publisher,
            quantity=new_book.quantity
        )
        db.session.add(insert_book)
        db.session.commit()
        return ReturnCode.SUCCESS

    @staticmethod
    def get_book(id):
        return Book.query.get(id)

    @staticmethod
    def update_book(id, book_request):
        book = Book.query.get(id)
        for key, value in book_request.items():
            setattr(book, key, value)
        db.session.commit()
        return ReturnCode.SUCCESS

    @staticmethod
    def delete_book(id):
        book = Book.query.get(id)
        if not book:
            return ReturnCode.BOOK_NOT_FOUND

        db.session.delete(book)
        db.session.commit()
        return ReturnCode.SUCCESS
