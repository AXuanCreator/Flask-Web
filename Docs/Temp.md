>  知识点：模板渲染，返回HTML格式文件 
>
>  代码位置：demo/demo_3/app.py 

## HTML

HTML用于创建网页，由一系列元素组成，这些元素用于描述页面的结构、内容、样式

以下是一个简单的HTML文件

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>This is a html file</title>
</head>
<body>
这是一个HTML文件
</body>
</html>
```

* <\!DOCTYPE html>：HTML5的文档类型声明，告诉浏览器使用HTML5规则解析此文档。**编译器自动生成**
* \<html lang="en">：HTML文档的根元素，表示这里是整个HTML文档的开始。`lang="en"`表示指定了文档语言为英文。**编译器自动生成**
* \<head>：这是HTML文档头部部分的开始，包含文档的元数据：字符集声明、标题、样式表等，而`</head>`表示HTML文档头部部分的结束。**编译器部分生成，需要手动填写一些元数据**
    * \<meta charset="UTF-8">：`<meta>`元素用于声明文档的字符集为UTF-8
    * \<title> This is a html file\</title>： `<title>`为标题元素的开始标签，`</title>`为标题元素的结束标签，里面填写文本，表示该HTML文档的标题
    * 