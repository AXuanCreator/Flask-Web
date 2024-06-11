import random
import re
import string
from datetime import datetime

import pandas as pd
from tqdm import tqdm

from Config import BookRating, db, Regex, User, UserConfig, Book, Borrow
from Code.app import create_app
from Utils import Helper

app = create_app()


def load_rating_with_csv():
    # 若无法找到路径，则表示没有将Code设置为源代码目录
    book_rating_csv = pd.read_csv('./Config/csv/goodread_dataset/ratings.csv')

    with app.app_context():
        for index, row in book_rating_csv.iterrows():
            # print(f'{row}')
            book_rating = BookRating(
                user_id=row['user_id'], book_id=row['book_id'], rating=row['rating'])
            db.session.add(book_rating)

        db.session.commit()


def load_book_with_csv():
    book_csv = pd.read_csv('./Dataset/csv/goodread_dataset/books.csv')

    with app.app_context():
        for index, row in tqdm(book_csv.iterrows(), desc='Load Book'):
            if pd.isna(row['original_title']):
                row['original_title'] = f'UNKNOWN_{index}'
            book = Book(title=row['original_title'], author=row[
                'authors'], publisher='Personal', quantity=random.randint(10, 80), category_id=random.randint(1, 12))

            try:
                db.session.add(book)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f'\033[36m[ERROR]\033[35m | ERROR : {e}')


# db.session.commit()


def load_borrow_with_csv():
    borrow_csv = pd.read_csv('./Dataset/csv/goodread_dataset/to_read.csv')

    with app.app_context():
        for index, row in tqdm(borrow_csv.iterrows(), desc='Load Borrow'):
            try:
                borrow = Borrow(user_id=row['user_id'], book_id=row['book_id'],
                                borrow_date=datetime(random.randint(
                                    2018, 2023), random.randint(1, 12), random.randint(1, 28)),
                                return_date=datetime(2024, random.randint(
                                    1, 5), random.randint(1, 28)),
                                really_return_date=datetime(2024, 6, 1))

                db.session.add(borrow)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f'\033[36m[ERROR]\033[35m | ERROR : {e}')


def create_random_user(nums=60000):
    with app.app_context():
        for i in tqdm(range(nums), desc="Create User Data"):
            user = User(username=Helper.generate_random_string_with_pattern(Regex.username_pattern, 6, 10),
                        password=Helper.generate_random_string_with_pattern(
                            Regex.password_pattern, 9, 19),
                        name=Helper.generate_random_string_with_choice(
                            Regex.name_pattern, 2, 4),
                        gender=random.choice(['男', '女', 'Lady', 'Man']),
                        phone=Helper.generate_random_string_with_choice(
                            string.digits, 11, 11),
                        email=Helper.generate_random_string_with_choice(string.digits, 7, 15) + '@' +
                        random.choice(
                            ['qq.com', '163.com', 'gmail.com', 'outlook.com', 'mail.com']),
                        max_borrow_days=UserConfig.MAX_BORROW_DAYS,
                        max_borrow_books=UserConfig.MAX_BORROW_BOOKS
                        )

            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f'\033[36m[ERROR]\033[35m | ERROR : {e}')


if __name__ == '__main__':
    # create_random_user()
    # load_book_with_csv()
    load_borrow_with_csv()
