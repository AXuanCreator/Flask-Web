#############################################################
# Demo_6 实现一个简单的蓝图功能
# 蓝图位于 from flask import Blueprint
#############################################################
from flask import Blueprint, Flask

app = Flask(__name__)

bp1 = Blueprint('bp1', __name__)
bp2 = Blueprint('bp2', __name__)


@bp1.route('/bp1')
def route_bp1():
    # 访问/bp1时
    return 'bp1'


@bp2.route('/bp2')
def route_bp2():
    # 访问/api/bp2时
    return 'bp2'


if __name__ == '__main__':
    # 将蓝图与app绑定
    app.register_blueprint(bp1)
    app.register_blueprint(bp2, url_prefix='/api')

    # 输出蓝图管理的路由
    print("App应用所拥有的路由框架 ： \n", app.url_map)

    app.run(debug=True)


def my_func_a():
    """这是一个函数"""
    pass


def my_func_b(x):
    """
    这是一个带参数的函数
    :param x: 我不知道
    :return: 我也不知道
    """
    pass
