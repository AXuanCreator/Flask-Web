from flask import Flask, Blueprint, request
from Utils import Response, ResponseCode

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
def user_login():
	if request.method == 'POST':
		user_request = request.get_json()
		username = user_request.get('username')
		password = user_request.get('password')

	# TEST
	return Response.response(ResponseCode.BAD_REQUEST, 'TEST', None)

@user_bp.route('/register', methods=['POST'])
def user_register():
	if request.method == 'POST':
		pass

@user_bp.route('/<id>/deregister', methods=['DELETE'])
def user_deregister(id):
	if request.method == 'DELETE':
		pass

@user_bp.route('/send-code', methods=['POST'])
def user_send_code():
	if request.method == 'POST':
		pass

@user_bp.route('/<mail>/code', methods=['POST'])
def user_verify_code(mail):
	if request.method == 'POST':
		pass

@user_bp.route('/<id>/password', methods=['PUT'])
def user_change_password(id):
	if request.method == 'PUT':
		pass

@user_bp.route('/<id>', methods=['GET', 'PUT'])
def user_info(id):
	if request == 'GET':
		pass
	elif request == 'PUT':
		pass
