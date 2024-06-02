#!/user/bin/env python3
# -*- coding: utf-8 -*-
from Config import Book, ReturnCode, db


class BookServices:

    # 插入书籍
    @staticmethod
    def insert_book(book_request):
        request_keys = ['title', 'author', 'category', 'publisher', 'quantity']
        title, author, category, publisher, quantity = (book_request.get(key) for key in request_keys)

        insert_book = Book(title=title, author=author, category=category, publisher=publisher, quantity=quantity)

        db.session.add(insert_book)
        db.session.commit()
        return ReturnCode.SUCCESS

    # 根据id获取书籍
    @staticmethod
    def get_book(id):
        return Book.query.get(id)

    # 根据关键词获取书籍
    @staticmethod
    def list_book(keywords, page, per_page):
        query = Book.query

        if 'title' in keywords:
            query = query.filter(Book.title.like(f"%{keywords['title']}%"))
        if 'author' in keywords:
            query = query.filter(Book.author.like(f"%{keywords['author']}%"))
        if 'publisher' in keywords:
            query = query.filter(Book.publisher.like(f"%{keywords['publisher']}%"))
        if 'category_id' in keywords and keywords['category_id'] is not None:
            query = query.filter(Book.category_id == keywords['category_id'])

        total = query.count()
        books = query.offset((page - 1) * per_page).limit(per_page).all()

        return books, total

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
