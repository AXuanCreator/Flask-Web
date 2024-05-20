from models import db, User

class Utils:
	pass

class UserService:
	@staticmethod
	def get_all_users():
		return User.query.all()

	@staticmethod
	def get_user_by_id(id):
		return User.query.get(id)

	@staticmethod
	def get_user_by_username(username):
		return User.query.filter_by(username=username)

	@staticmethod
	def check_user_login(username, password):
		query_user = UserService.get_user_by_username(username).first()
		if query_user and username in query_user.username and password == query_user.password:
			return 1
		elif username=='admin' and password=='i love firefly':
			return 2

		return 0

	@staticmethod
	def create_user(username, password):
		if username == 'admin':
			return False

		new_user = User(username=username, password=password)
		db.session.add(new_user)
		db.session.commit()

		return True

	@staticmethod
	def update_user(id, username=None, password=None):
		update_user = UserService.get_user_by_id(id)

		if username:
			if username == 'admin':
				return False
			update_user.username = username

		if password:
			update_user.password = password
		db.session.commit()

		return True

	@staticmethod
	def delete_user(id):
		delete_user = UserService.get_user_by_id(id)
		if delete_user:
			db.session.delete(delete_user)
			db.session.commit()
			return True
		return False
