from flask import Flask, request

# 创建Flask应用实例
app = Flask(__name__)


### 知识点 [更详细的请看Docs文档的Demo解析]
# URL 与 视图函数
# URL的组成：协议+主机+端口+路径+查询字符串+锚点
# http协议，端口号默认为80
# https协议的默认端口号为443
# 如：https://www.baidu.com:443/path是百度的网址，但是即使不加端口号443，浏览器依旧可以识别协议并自动添加
# 因此，主要修改的是路径， URL 与 视图 也可以称之为 Path 与 视图


## 无参URL
@app.route('/')  # str内容实际就是Path，此时代表根路径。在进入根路径时，执行下面的视图函数
def hello_world():
	return 'Hello, World!'


@app.route('/firefly')  # 在进入firefly路径时，执行下面视图函数
def firefly():
	return 'Firefly!'


## 有参URL——使用<>来表示参数
# <>内的内容是参数，参数可以在函数中使用
@app.route('/firefly/<ff_id>')
def firefly_id(ff_id):
	if ff_id == 'SAM':  # <== :P 此处与本文知识点无关，但他会返回图片                                                                                                                                                                                                                                   为啥不试试呢？流萤小姐的盛世美貌盖世无双！
		return f'<html><body><img src="https://axuan-picture.oss-cn-guangzhou.aliyuncs.com/sam.png"></body></html>'
	else:
		return 'Firefly ID: %s' % ff_id


@app.route('/firefly/<ff_id>/<int:ff_num>')  # ff_id不限制类型，而ff_num必须为整数
def firefly_id_num(ff_id, ff_num):
	return 'Firefly ID: %s, Num: %d' % (ff_id, ff_num)


##  有参URL——使用?来表示参数
# 此时可以通过 ? 后面的参数来传递参数,如https://127.0.0.1:5000/book/list?page=2
# ? 后面的内容是参数，参数可以在函数中使用，需要从flask中导入request
@app.route('/book/list')  # 注意，这里并没有使用<>来表示参数
def book_list():  # 注意，这里并没有传入参数
	# request.args是一个字典，存储了所有的查询字符串参数
	# 使用get方法获取'page'参数，如果没有则默认为1，类型为int
	page = request.args.get('page', default=1, type=int)

	return f'Book List, Page: {page} || Request.args: {request.args}'


if __name__ == '__main__':
	# Debug模式
	app.run(debug=True)
