############################### VERSION 1.0 ###############################
# 用于管理返回给前端的JSON格式                                                                                                                                                                   流萤小姐与你同在
############################### VERSION 1.0 ###############################
from flask import jsonify


class Response:
	@staticmethod
	def response(code, msg, result):
		return jsonify({
			'code': code,
			'message': msg,
			'result': result
		})


class ResponseCode:
	BAD_REQUEST = 400
	USERNAME_REPEATED = 401
	USERNAME_NOT_ALLOW = 402
	MAIL_NOT_ALLOW = 403
	MAIL_REPEATED = 404

	SUCCESS = 500
	FAILED = 501
	OUT_TIME = 502

	BOOK_NOT_EXIST = 601
	BOOK_UNAVAILABLE = 602
	BORROW_LIMITED = 603
	BORROW_ALREADY = 604
	BOOK_ALREADY_EXIT = 605
	RETURN_OVERDUE = 606
	RETURN_ALREADY = 607

	LOGIN_SUCCESS = 700
	ACCOUNT_NOT_EXIST = 701
	WRONG_PASSWORD = 702    # TODO:改为PASSWORD_WRONG
