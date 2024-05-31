from Config import BookCategory, ReturnCode, db


class BookCategoryServices:
    @staticmethod
    def add_book_category(category_request):
        name = category_request.get('name')
        if BookCategory.query.filter_by(name=name).first():
            return ReturnCode.CATEGORY_ALREADY_EXISTS

        new_category = BookCategory(**category_request)
        db.session.add(new_category)
        db.session.commit()
        return ReturnCode.SUCCESS

    @staticmethod
    def get_book_category(id):
        return BookCategory.query.get(id)

    @staticmethod
    def update_book_category(id, category_request):
        category = BookCategory.query.get(id)
        if not category:
            return ReturnCode.CATEGORY_NOT_FOUND

        for key, value in category_request.items():
            setattr(category, key, value)
        db.session.commit()
        return ReturnCode.SUCCESS

    @staticmethod
    def delete_book_category(id):
        category = BookCategory.query.get(id)
        if not category:
            return ReturnCode.CATEGORY_NOT_FOUND

        db.session.delete(category)
        db.session.commit()
        return ReturnCode.SUCCESS
