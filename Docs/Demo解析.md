# Demo_1

>  知识点 ： Debug模式 ||  Host修改 ||  Port修改 

## Debug模式

开启Debug模式后，在修改代码后会自动重新加载

两种调用方式:

1. 在app.run中传入debug参数

    ```python
    if __name__ == '__main__':
    	app.run(debug=True)
    ```

2. PyCharm的脚本编辑中添加

    <img src="Demo解析.assets/image-20240515163703241.png" alt="image-20240515163703241" style="zoom: 50%;" />

## Host修改

修改Host的作用是：让同一 **局域网** 下的电脑可以通过IP访问到我电脑上的Flask-Web应用

在无参数启动Flask时，它的Host为 `127.0.0.1`

![image-20240515171211543](Demo解析.assets/image-20240515171211543.png)

可以通过向app.run()传入参数修改host

1. 通过CMD得知自己的IP地址

    ```cmd
    ipconfig
    ```

    ![image-20240515171924025](Demo解析.assets/image-20240515171924025.png)

2. 给app.run传入参数

    ```python
    if __name__ == '__main__':
    	app.run(host='xx.xx.xx.xx')
    ```

![image-20240515172103579](Demo解析.assets/image-20240515172103579.png)

## Port修改

作用：当默认端口5000端口被其他程序占用时，通过修改Port来监听

在无参数启动时，默认端口是 `5000`

可通过向app.run()传入参数修改Port

```python
if __name__ == '__main__':
	app.run(port=5001)
```

![image-20240515172420762](Demo解析.assets/image-20240515172420762.png)
