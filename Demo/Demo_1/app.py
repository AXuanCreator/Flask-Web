from flask import Flask

# 使用Flask类创建app对象
# __name__表示当前模块
app = Flask(__name__)

# 创建路由和视图函数映射
# @app.rout('/')表示根路由
# 当用户访问 http://127.0.0.1:5000/ 时，会执行hello_world函数
@app.route('/')
def hello_world():  # put application's code here
    return '流萤小姐美貌盖世无双'


if __name__ == '__main__':
    # 无参数启动
    app.run()

    # Debug模式
    # app.run(debug=True)

    # 修改主机
    # app.run(host='xx.xx.xx.xx')

    # 修改端口号
    # app.run(port=5001)
