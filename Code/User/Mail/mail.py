import random

from flask_mail import Mail, Message
from Config import ReturnCode, UserConfig

mail = Mail()
code_recorder = {}


class SendMail:
	@staticmethod
	def send_mail(recipient, body=None, html_body=None):
		"""
		邮件发送
		:param subject: 邮件主题
		:param recipient: 收件人邮箱
		:param body: 正文内容,默认为None
		:param html_body：以HTML形式发送，默认为None
		:return:
		"""
		message = Message('Your Code', recipients=[recipient])
		message.body = code_recorder[recipient]

		if html_body:
			message.html = html_body

		try:
			mail.send(message)
			return True
		except Exception as e:
			print('\033[36m[ERROR]\033[0m | SendMail : ', str(e))
			return False

	@staticmethod
	def generate_random_code(mail):
		# 从MAIL_CODE中获取长度为MAIL_CODE_LEN的验证码
		code = ''.join(random.choices(UserConfig.MAIL_CODE, k=UserConfig.MAIL_CODE_LEN))
		print('\033[35m[DEBUG]\033[0m | Generate Code : ', code)

		code_recorder[mail] = code
		print('\033[35m[DEBUG]\033[0m | Code Recorder : ', code_recorder)

	@staticmethod
	def remove_code(mail):
		print('\033[35m[DEBUG]\033[0m | Remove Code Task Start')
		try:
			del code_recorder[mail]
		except Exception as e:
			print('\033[36m[ERROR]\033[0m | Remove Code Fail')

