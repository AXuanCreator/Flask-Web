# Flask-Web

## 项目介绍

占位---

你是否承认，流萤小姐的盛世美貌盖世无双!



## 环境配置

**Windows 11**

**PyCharm**

1. 下载Miniconda

    ```
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
    ```

    * 安装勾选时建议三个全部勾选
    * **务必记得安装路径**

    

2. 将Miniconda添加至环境变量中

    * 按下Windows键，在搜索框内搜索 **编辑系统环境变量**，选择 **环境变量(N)...**

        <img src="README.assets/image-20240515144616447.png" alt="image-20240515144616447" style="zoom:50%;" />

        <img src="README.assets/image-20240515145018687.png" alt="image-20240515145018687" style="zoom: 80%;" />

    * 找到 **系统变量(S)** 中的 `Path`，并双击进入

        <img src="README.assets/image-20240515145055234.png" alt="image-20240515145055234" style="zoom:67%;" />

    * 点击 **新建(N)**，添加两条环境变量:

        <img src="README.assets/image-20240515145111500.png" alt="image-20240515145111500" style="zoom:67%;" />

        ```bash
        PATH\condabin
        PATH\Scripts
        
        ### 举例 ###
        # PATH为Miniconda的安装路径
        # 假设：PATH为D:\Program_Work\Setup-Miniconda
        
        # 添加环境变量
        D:\Program_Work\Setup-Miniconda\condabin
        D:\Program_Work\Setup-Miniconda\Scripts
        ```

    

3. 打开CMD并导航到项目目录

    ```bash
    cd /PATH/TO/Project
    
    # 查看Conda是否成功安装
    conda --version
    ```

    

4. 创建虚拟环境

    ```bash
    conda create -n flask-web python=3.10 -y
    
    conda activate flask-web
    
    conda install flask -y 
    ```

    

5. 编译器配置

    * 下载安装Pycharm Community

        ```bash
        # 下载地址
        https://download-cdn.jetbrains.com/python/pycharm-community-2024.1.1.exe
        ```
        
    * [Optional] 添加插件

        * 快捷键 `Ctrl + ,` 打开设置
        
        * 选择 **Plugins > Marketplace**
        
            <img src="README.assets/image-20240515153109264.png" alt="image-20240515153109264" style="zoom:50%;" />
        
            * 好用的插件有 : `Chinese`，`Github Theme`，`Rainbow Brackets`，`VSCode Keymap`，`CodeGlance Pro`
        
    * 在编译器内添加虚拟环境
    
        * 新建/打开已有项目
        
        * 快捷键 `Ctrl + ,` 打开设置
        
        * 点击 **项目:[你的项目名]** >  **Python解释器 ** >  **添加解释器**  >  **添加本地解释器**
        
            <img src="README.assets/image-20240515142817461.png" alt="image-20240515142817461" style="zoom:80%;" />
        
        * 左边选择 **Conda环境**，可执行文件选择`[Path_To_Miniconda]\Scripts\conda.exe`
        
            <img src="README.assets/image-20240515143211684.png" alt="image-20240515143211684" style="zoom: 50%;" />
        
            <img src="README.assets/image-20240515143734908.png" alt="image-20240515143734908" style="zoom:50%;" />
        
            <img src="README.assets/image-20240515143820890.png" alt="image-20240515143820890" style="zoom: 50%;" />
        
        * 选择 **使用现有环境** ，在下拉框中选择 `flask-web`，点击确认
        
            <img src="README.assets/image-20240515144222714.png" alt="image-20240515144222714" style="zoom: 50%;" />
        
            
    
    

## [Optional] 测试

1. 在项目目录下新建`test.py`，并复制以下内容
   
    ```python
    from flask import Flask
      
    # 创建Flask应用实例
    app = Flask(__name__)
      
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
      
    if __name__ == '__main__':
        app.run(debug=True)
    ```

2. 选择PyCharm上方的 **当前文件 > 编辑配置**

	<img src="README.assets/image-20240515145549662.png" alt="image-20240515145549662" style="zoom:80%;" />

3. 点击 **+号**，并选择 **Flask服务器**

    <img src="README.assets/image-20240515150021871.png" alt="image-20240515150021871" style="zoom:50%;" />

4. 填写相应信息

    <img src="README.assets/image-20240515150700126.png" alt="image-20240515150700126" style="zoom:50%;" />

5. Debug，并打开网址:http://127.0.0.1:5000，显示`Hello World`
   
    <img src="README.assets/image-20240515150820288.png" alt="image-20240515150820288" style="zoom: 80%;" />

​       



## Flask-Web项目构建

--> ./Docs (temp)





















