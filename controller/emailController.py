import email
import smtplib

#发送email
#email_content eamil字典
def send(email_content):
	contents = email_content['content']
	content = ''
	for c in contents:
		content += (c + '\n')
	msg = email.message_from_string(content)
	msg['From'] = "1716030824@qq.com"
	msg['To'] = "zhoum1118@163.com"
	msg['Subject'] = email_content['subject']
	try:
		#设置发送邮件服务器，在你的发送邮箱中的设置中去开启
		s = smtplib.SMTP("smtp.qq.com",25)
		# 要发送此命令的主机名默认为本地主机的完全限定域名。
		s.ehlo()
		s.starttls() #Puts connection to SMTP server in TLS mode
		s.ehlo()
		s.login('1716030824@qq.com', 'klxptdumbhspbiib')
		s.sendmail("1716030824@qq.com", "zhoum1118@163.com", msg.as_string().encode('utf-8'))
		s.quit()
		return True
	except:
		print('send email fail!')
		return False

if __name__ == "__main__":
	subject = '测试邮件2'
	content = ['第2封测试邮件！hello python!']
	email_c = {}
	email_c['subject'] = subject
	email_c['content'] = content
	print(send(email_c))