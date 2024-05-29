from flask import Flask, Blueprint

admin_bp = Blueprint('admin', __name__)

# @book_bp.route('/example', methods=['GET'])