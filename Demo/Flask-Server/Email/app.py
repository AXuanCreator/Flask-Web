from flask import Flask, render_template_string, request
from flask_mail import Mail, Message

app = Flask(__name__)

# 配置 Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.sinpor.top'  # 邮件服务器地址
app.config['MAIL_PORT'] = 587  # 邮件服务器端口
app.config['MAIL_USE_TLS'] = True  # 启用 TLS
app.config['MAIL_USE_SSL'] = False  # 不启用 SSL
app.config['MAIL_USERNAME'] = 'eigb903@sinpor.top'  # 你的邮件用户名
app.config['MAIL_PASSWORD'] = 'sinpor123'  # 你的邮件密码
app.config['MAIL_DEFAULT_SENDER'] = ('Coder', 'eigb903@sinpor.top')  # 默认发件人

mail = Mail(app)

@app.route('/')
def index():
	return render_template_string('''
        <form action="/send-mail" method="POST">
            <input type="email" name="email" placeholder="Recipient Email">
            <input type="text" name="subject" placeholder="Subject">
            <textarea name="body" placeholder="Message Body"></textarea>
            <button type="submit">Send Email</button>
        </form>
    ''')

@app.route('/send-mail', methods=['POST'])
def send_mail():
	email = request.form['email']
	subject = request.form['subject']
	body = request.form['body']

	msg = Message(subject, recipients=[email], body=body)
	mail.send(msg)
	return 'Mail sent!'

if __name__ == '__main__':
	app.run(debug=True)
