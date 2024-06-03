#!/user/bin/env python3
# -*- coding: utf-8 -*-
from Config import Book, ReturnCode, db, BookCategory


class BookServices:

	@staticmethod
	def insert_book(book_request):
		"""插入书籍"""
		request_keys = ['title', 'author', 'category', 'publisher', 'quantity']
		title, author, category_id, publisher, quantity = (book_request.get(key) for key in request_keys)

		if any(var is None for var in [title, author, category_id, publisher, quantity]):
			return ReturnCode.FAIL

		insert_book = Book(title=title, author=author, category_id=category_id, publisher=publisher, quantity=quantity)

		db_category = BookCategory.query.get(category_id)
		if db_category is None:
			return ReturnCode.FAIL
		db_category.quantity += 1

		db.session.add(insert_book)
		db.session.commit()

		return ReturnCode.SUCCESS

	@staticmethod
	def get_book(id):
		"""根据id获取书籍"""
		return Book.query.get(id)

	@staticmethod
	def list_book(keywords, page, per_page):
		"""根据关键词获取书籍列表"""
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

	@staticmethod
	def update_book(id, update_data):
		"""更新书籍信息"""
		book = Book.query.get(id)
		if 'title' in update_data:
			book.title = update_data['title']
		if 'author' in update_data:
			book.author = update_data['author']
		if 'publisher' in update_data:
			book.publisher = update_data['publisher']
		if 'quantity' in update_data:
			book.quantity = update_data['quantity']
		if 'category_id' in update_data:
			db_category = BookCategory.query.get(book.category_id)
			if db_category is None:
				return ReturnCode.FAIL
			db_category.quantity -= 1

			book.category_id = update_data['category_id']
			new_db_category = BookCategory.query.get(book.category_id)  # 获取新分类的id
			if new_db_category is None:
				return ReturnCode.FAIL
			new_db_category.quantity += 1

		db.session.add(book)
		db.session.commit()

		return ReturnCode.SUCCESS

	@staticmethod
	def delete_book(id):
		"""删除书籍"""
		book = Book.query.get(id)
		if not book:
			return ReturnCode.BOOK_NOT_EXIST

		book_category_id = book.get('category_id')
		db_category = BookCategory.query.get(book_category_id)

		if db_category is None:
			return ReturnCode.FAIL

		db_category.quantity -= 1  # 对应分类的数量-1
		db.session.delete(book)
		db.session.commit()

		return ReturnCode.SUCCESS
