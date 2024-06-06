# Flask-Web

## 项目介绍

本项目为 **图书管理系统** ，类似于[Z-Library](https://z-library.cc/)或[豆瓣读书](https://book.douban.com/)等网站

</br>

看点：

* 基于深度学习的图书推荐(测试中)
* 邮箱验证码
* 登陆保持
* ....

</br>

目前 **Main分支** 为前后端分离版本，而 **Jinja分支** 使用Jinja2引擎渲染静态模板，即前后端不分离，是目前主要开发的方向

</br>

Code目录下为Flask-Web本体，其余是演示项目及教程文档

</br>

感谢  [YuXeng](https://github.com/YusJade) 与 [Serendipity](https://github.com/Serendipity-hjn) 对本项目的贡献

</br>

</br>



## 预览

此预览为 **Jinja** 分支内容

<img src="./Docs/assets/alpha1.gif" alt="alpha1" style="zoom:50%;" />

</br>

</br>

## 运行

TODO：将会提供可执行文件

1. 安装Miniconda，详细看 [安装Miniconda](./Docs/环境配置.md#安装Miniconda)

2. 安装PyCharm，详细看 [安装PyCharm](./Docs/环境配置.md#安装PyCharm)

3. 创建虚拟环境

    ```cmd
    # 一下命令在终端运行
    conda create -n flask-web python=3.10 -y
    conda activate flask-web
    conda install flask pymysql flask-sqlalchemy flask_cors  -y 
    pip install flask-migrate flask_caching
    conda install pytorch tqdm pandas -y 	# 深度学习框架，可能会较大
    ```

4. 在PyCharm中启用该虚拟环境，详细看[PyCharm虚拟环境](./Docs/环境配置.md#在PyCharm内添加虚拟环境)

5. 在 **Code/Config/config.py**中填写数据库登陆信息

6. 运行 **app.py** 脚本

    ```cmd
    在编译器中配置运行脚本，工作目录选择Code文件夹
    ```

    

    





## 项目文件结构(即将废弃)

Flask-Web

——Code **Flask-Web主要代码**

——Demo **例子**

————Demo_1 **Debug模式、Host | Port修改**

————Demo_2 **URL与视图函数**

————Demo_3 **Flask与数据库的连接 | ORM模型**

————Demo_4 **ORM模型外键与表的关系**

————Demo_5 **更好的ORM模型映射表的方法**

————Demo_6 **使用蓝图管理URL**

————Flask-Server **使用Flask框架写的组件**

————————AdminLogin **管理员登陆操作组件**

</br>

——Docs **文档**

————QA.md **项目出现报错时可以到这个文件 Ctrl + F 搜索一下**

————Demo解析.md **Demo的例子解析，认真阅读即可熟悉Flask框架**(即将废弃)

————扩展信息.md **杂项**



















