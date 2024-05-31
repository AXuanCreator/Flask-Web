from flask import Blueprint, request
from Config import ReturnCode, BookCategory, db
from Utils import Response, ResponseCode
from .bookcategory_services import BookCategoryServices

bookcategory_bp = Blueprint('book category', __name__)


@bookcategory_bp.route('/book-category', methods=['POST'])
def add_book_category():
    category_request = request.get_json()
    match BookCategoryServices.add_book_category(category_request):
        case ReturnCode.SUCCESS:
            return Response.response(ResponseCode.SUCCESS, 'Category added successfully', None)
        case ReturnCode.CATEGORY_ALREADY_EXISTS:
            return Response.response(ResponseCode.CATEGORY_ALREADY_EXISTS, 'Category already exists', None)
        case _:
            return Response.response(ResponseCode.BAD_REQUEST, 'Bad request', None)


@bookcategory_bp.route('/book-category/<int:id>', methods=['GET'])
def get_book_category(id):
    category = BookCategoryServices.get_book_category(id)
    if category:
        return Response.response(ResponseCode.SUCCESS, 'Category found', category)
    else:
        return Response.response(ResponseCode.NOT_FOUND, 'Category not found', None)


@bookcategory_bp.route('/book-category/<int:id>', methods=['PUT'])
def update_book_category(id):
    category_request = request.get_json()
    match BookCategoryServices.update_book_category(id, category_request):
        case ReturnCode.SUCCESS:
            return Response.response(ResponseCode.SUCCESS, 'Category updated successfully', None)
        case ReturnCode.CATEGORY_NOT_FOUND:
            return Response.response(ResponseCode.NOT_FOUND, 'Category not found', None)
        case _:
            return Response.response(ResponseCode.BAD_REQUEST, 'Bad request', None)


@bookcategory_bp.route('/book-category/<int:id>', methods=['DELETE'])
def delete_book_category(id):
    match BookCategoryServices.delete_book_category(id):
        case ReturnCode.SUCCESS:
            return Response.response(ResponseCode.SUCCESS, 'Category deleted successfully', None)
        case ReturnCode.CATEGORY_NOT_FOUND:
            return Response.response(ResponseCode.NOT_FOUND, 'Category not found', None)
        case _:
            return Response.response(ResponseCode.BAD_REQUEST, 'Bad request', None)
