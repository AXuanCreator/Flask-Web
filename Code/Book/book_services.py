#!/user/bin/env python3
# -*- coding: utf-8 -*-
from Config import Book, ReturnCode, db


class BookServices:

    # 插入书籍
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

    # 根据id获取书籍
    @staticmethod
    def get_book(id):
        return Book.query.get(id)

    # 更新书籍信息
    @staticmethod
    def update_book(id, update_data):
        book = Book.query.get(id)
        if 'title' in update_data:
            book.title = update_data['title']
        if 'author' in update_data:
            book.author = update_data['author']
        if 'category_id' in update_data:
            book.category_id = update_data['category_id']
        if 'publisher' in update_data:
            book.publisher = update_data['publisher']
        if 'quantity' in update_data:
            book.quantity = update_data['quantity']
        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def delete_book(id):
        book = Book.query.get(id)
        if not book:
            return ReturnCode.BOOK_NOT_EXIST

        db.session.delete(book)
        db.session.commit()
        return ReturnCode.SUCCESS
