from Config import BookCategory, ReturnCode, db


class BookCategoryServices:
    @staticmethod
    def insert_book_category(name_data):
        name = name_data
        if BookCategory.query.filter_by(name=name).first():
            return ReturnCode.CATEGORY_EXIST

        new_book_category = BookCategory(name=name_data)

        db.session.add(new_book_category)
        db.session.commit()
        return ReturnCode.SUCCESS

    # 分页显示全部分类
    @staticmethod
    def list_book_categories(page, per_page):
        categories_query = BookCategory.query
        total = categories_query.count()
        categories = categories_query.offset((page - 1) * per_page).limit(per_page).all()
        return categories, total

    # 根据名字搜索类别
    @staticmethod
    def get_book_category_by_name(name):
        return BookCategory.query.filter_by(name=name).first()

    # 类别信息更新
    @staticmethod
    def update_book_category(id, category_name):
        category = BookCategory.query.get(id)
        category.name = category_name
        db.session.commit()

        return category

    # 类别删除
    @staticmethod
    def delete_book_category(id):
        category = BookCategory.query.get(id)
        if category is None:
            return ReturnCode.CATEGORY_NOT_EXIST
        db.session.delete(category)
        db.session.commit()
        return ReturnCode.SUCCESS
