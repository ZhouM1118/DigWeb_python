import email
import smtplib

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
		s = smtplib.SMTP("smtp.qq.com",25)
		s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
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
	email = {}
	email['subject'] = subject
	email['content'] = content
	print(send(email))