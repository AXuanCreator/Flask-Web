from flask import Flask, Blueprint

book_bp = Blueprint('book', __name__)

# @book_bp.route('/example', methods=['GET'])